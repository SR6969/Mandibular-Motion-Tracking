import bpy
import csv

csv_file = r"C:\Users\sathv\Downloads\jaw_motion.csv"

obj = bpy.data.objects["LowerJaw"]

scale = 0.01      # Change if movement is too large/small

with open(csv_file, newline='') as f:
    reader = csv.DictReader(f)

    for row in reader:

        frame = int(row["Frame"])

        x = float(row["Jaw_X"]) * scale
        y = float(row["Jaw_Y"]) * scale
        z = float(row["Jaw_Z"]) * scale

        bpy.context.scene.frame_set(frame)

        obj.location.x = x
        obj.location.y = y
        obj.location.z = z

        obj.keyframe_insert(data_path="location")