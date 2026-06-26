# JAW TRACKING V3
# Reference landmarks fixed at origin:
# Front: Nose = (0,0)
# Side: Ear = (0,0)

import cv2
import numpy as np
import pandas as pd
import math

try:
    TRACKER = cv2.legacy.TrackerCSRT_create
except:
    TRACKER = cv2.TrackerCSRT_create

TRACK_BOX = 60

class Kalman2D:
    def __init__(self):
        self.k = cv2.KalmanFilter(4,2)
        self.k.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]], np.float32)
        self.k.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], np.float32)
        self.k.processNoiseCov = np.eye(4,dtype=np.float32)*1e-3

    def update(self,x,y):
        self.k.correct(np.array([[np.float32(x)],[np.float32(y)]]))
        p=self.k.predict()
        return float(p[0,0]), float(p[1,0])

def select_points(frame,names):
    pts=[]
    img=frame.copy()

    def cb(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN and len(pts)<len(names):
            pts.append((x,y))

    cv2.namedWindow("Select")
    cv2.setMouseCallback("Select",cb)

    while True:
        d=img.copy()
        for i,p in enumerate(pts):
            cv2.circle(d,p,5,(0,255,0),-1)
            cv2.putText(d,names[i],p,0,0.6,(0,255,0),2)

        cv2.imshow("Select",d)

        if cv2.waitKey(20)&0xFF==13 and len(pts)==len(names):
            break

    cv2.destroyWindow("Select")
    return pts

def create_tracker(frame,p):
    t=TRACKER()
    t.init(frame,(p[0]-30,p[1]-30,TRACK_BOX,TRACK_BOX))
    return t

def process_front(video):
    cap=cv2.VideoCapture(video)
    fps=max(cap.get(cv2.CAP_PROP_FPS),1)
    ok,frame=cap.read()
    if not ok:
        return

    nose,chin=select_points(frame,["Nose","Chin"])

    tr_nose=create_tracker(frame,nose)
    tr_chin=create_tracker(frame,chin)

    knose=Kalman2D()
    kchin=Kalman2D()

    h,w=frame.shape[:2]
    writer=cv2.VideoWriter("tracked_front.mp4",
                           cv2.VideoWriter_fourcc(*'mp4v'),
                           fps,(w,h))

    rows=[]
    frame_no=0

    while True:
        ok,frame=cap.read()
        if not ok:
            break

        _,b1=tr_nose.update(frame)
        _,b2=tr_chin.update(frame)

        nx,ny=b1[0]+b1[2]/2,b1[1]+b1[3]/2
        cx,cy=b2[0]+b2[2]/2,b2[1]+b2[3]/2

        nx,ny=knose.update(nx,ny)
        cx,cy=kchin.update(cx,cy)

        relx=cx-nx
        rely=cy-ny
        err=math.sqrt(relx**2+rely**2)

        cv2.circle(frame,(int(nx),int(ny)),6,(0,255,0),-1)
        cv2.circle(frame,(int(cx),int(cy)),6,(0,0,255),-1)
        cv2.line(frame,(int(nx),int(ny)),(int(cx),int(cy)),(255,255,0),2)

        cv2.putText(frame,f"Frame:{frame_no}",(20,30),0,0.7,(255,255,255),2)
        cv2.putText(frame,f"Jaw:{err:.2f}",(20,60),0,0.7,(255,255,255),2)

        cv2.imshow("Front Tracking",frame)
        writer.write(frame)

        rows.append([
            frame_no,
            frame_no/fps,
            0,0,
            relx,rely,
            relx,rely,
            err,
            err
        ])

        k=cv2.waitKey(1)&0xFF
        if k==27:
            break

        frame_no+=1

    pd.DataFrame(rows,columns=[
        "Frame","Time",
        "Nose_X","Nose_Y",
        "Chin_Relative_X","Chin_Relative_Y",
        "Relative_X","Relative_Y",
        "Jaw_Opening","Error_Front"
    ]).to_excel("front_view.xlsx",index=False)

    cap.release()
    writer.release()

def process_side(video,excel_name,video_name):
    cap=cv2.VideoCapture(video)
    fps=max(cap.get(cv2.CAP_PROP_FPS),1)

    ok,frame=cap.read()
    if not ok:
        return

    ear,chin,mandible=select_points(frame,["Ear","Chin","Mandible"])

    tr_ear=create_tracker(frame,ear)
    tr_chin=create_tracker(frame,chin)
    tr_man=create_tracker(frame,mandible)

    k1,k2,k3=Kalman2D(),Kalman2D(),Kalman2D()

    h,w=frame.shape[:2]
    writer=cv2.VideoWriter(video_name,
                           cv2.VideoWriter_fourcc(*'mp4v'),
                           fps,(w,h))

    rows=[]
    f=0

    while True:
        ok,frame=cap.read()
        if not ok:
            break

        _,b1=tr_ear.update(frame)
        _,b2=tr_chin.update(frame)
        _,b3=tr_man.update(frame)

        ex,ey=k1.update(b1[0]+b1[2]/2,b1[1]+b1[3]/2)
        cx,cy=k2.update(b2[0]+b2[2]/2,b2[1]+b2[3]/2)
        mx,my=k3.update(b3[0]+b3[2]/2,b3[1]+b3[3]/2)

        chin_relx = cx-ex
        chin_rely = cy-ey

        mand_relx = mx-ex
        mand_rely = my-ey

        err=math.sqrt(chin_relx**2+chin_rely**2)

        cv2.circle(frame,(int(ex),int(ey)),6,(0,255,0),-1)
        cv2.circle(frame,(int(cx),int(cy)),6,(0,0,255),-1)
        cv2.circle(frame,(int(mx),int(my)),6,(255,0,0),-1)

        cv2.line(frame,(int(ex),int(ey)),(int(cx),int(cy)),(255,255,0),2)

        cv2.putText(frame,f"Ear-Chin Error:{err:.2f}",(20,30),0,0.7,(255,255,255),2)

        cv2.imshow(video_name,frame)
        writer.write(frame)

        rows.append([
            f,
            f/fps,
            0,0,
            chin_relx,chin_rely,
            mand_relx,mand_rely,
            mand_relx,mand_rely,
            err
        ])

        f+=1

        if cv2.waitKey(1)&0xFF==27:
            break

    pd.DataFrame(rows,columns=[
        "Frame","Time",
        "Ear_X","Ear_Y",
        "Chin_Relative_X","Chin_Relative_Y",
        "Mandible_Relative_X","Mandible_Relative_Y",
        "Mandible_X","Mandible_Y",
        "Error_Ear_Chin"
    ]).to_excel(excel_name,index=False)

    cap.release()
    writer.release()

if __name__=="__main__":
    process_front(r"C:\Users\sathv\Downloads\middle4.mp4")
    process_side(r"C:\Users\sathv\Downloads\left4.mp4","left_view.xlsx","tracked_left.mp4")
    process_side(r"C:\Users\sathv\Downloads\right4.mp4","right_view.xlsx","tracked_right.mp4")

    cv2.destroyAllWindows()
