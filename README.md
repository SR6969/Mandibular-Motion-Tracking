# Mandibular Motion Tracking System

## Overview

This project is a computer vision-based mandibular motion tracking system developed to analyze lower jaw movement from synchronized frontal and lateral facial videos. The system tracks anatomical landmarks, compensates for head motion using stable reference landmarks, computes mandibular displacement, exports motion data to Excel/CSV, and generates Blender-compatible motion data for 3D visualization.

The project is intended for research and educational applications in biomechanics, dentistry, maxillofacial studies, and computer vision.

---

## Features

* Multi-view mandibular motion tracking
* Frontal, left-side, and right-side video processing
* Manual landmark initialization
* KCF/CSRT tracker-based landmark tracking
* Kalman filter for landmark smoothing
* Head-motion compensation using reference landmarks
* Jaw displacement and error calculation
* Excel (.xlsx) export
* CSV export for Blender
* Real-time tracking visualization
* Processed video generation with tracking overlays
* Blender-compatible lower jaw animation

---

## Tracking Methodology

### Frontal View

**Reference Landmark**

* Nose Tip

**Tracked Landmark**

* Chin Center

The nose is treated as the fixed reference point, and jaw motion is computed relative to the nose.

Outputs include:

* Relative X displacement
* Relative Y displacement
* Jaw opening distance
* Tracking error

---

### Left Side View

**Reference Landmark**

* Ear

**Tracked Landmarks**

* Chin
* Mandible (Gonion)

The ear acts as the fixed cranial reference. Chin and mandible movements are tracked relative to the ear.

Outputs include:

* Chin relative coordinates
* Mandible relative coordinates
* Ear–Chin tracking error

---

### Right Side View

The same methodology as the left-side view is used.

---

## Output Files

The program generates:

```text
front_view.xlsx
left_view.xlsx
right_view.xlsx

tracked_front.mp4
tracked_left.mp4
tracked_right.mp4
```

These files contain tracked landmark coordinates, relative mandibular motion, and processed tracking videos.

---

## Blender Pipeline

The exported tracking data is converted into a single motion file containing:

* Jaw_X
* Jaw_Y
* Jaw_Z

This file is imported into Blender to animate a simplified lower jaw model (represented by a sphere or jaw object).

Only the lower jaw moves while the reference skull remains fixed.

---

## Technologies Used

* Python
* OpenCV
* NumPy
* Pandas
* OpenPyXL
* Blender
* KCF / CSRT Tracker
* Kalman Filtering

---

## Project Workflow

```text
Input Videos
      │
      ▼
Manual Landmark Selection
      │
      ▼
Landmark Tracking
      │
      ▼
Head Motion Compensation
      │
      ▼
Jaw Motion Calculation
      │
      ▼
Excel / CSV Export
      │
      ▼
Blender Animation
```

---

## Repository Structure

```text
Mandibular-Motion-Tracking/

│── tracking/
│     jaw_tracking.py

│── blender/
│     blender_animation.py

│── data/
│     sample_videos/

│── images/

│── README.md

│── requirements.txt
```

---

## Installation

Install the required Python packages:

```bash
pip install opencv-contrib-python numpy pandas openpyxl matplotlib
```

---

## Usage

1. Run the Python tracking script.
2. Select the required anatomical landmarks.
3. Process the frontal and side-view videos.
4. Export the generated Excel/CSV files.
5. Import the generated motion data into Blender.
6. Animate the lower jaw model.

---

## Applications

* Mandibular motion analysis
* Dental biomechanics
* Maxillofacial research
* Computer vision
* Biomedical engineering
* Medical animation
* Motion tracking research

---

## Future Improvements

* Automatic facial landmark detection using MediaPipe Face Mesh
* 3D mandibular reconstruction
* Real-world metric calibration
* Deep learning-based landmark tracking
* Real-time Blender integration
* Clinical jaw movement analysis

---

## License

This project is intended for academic and research purposes. Feel free to use, modify, and extend the code with appropriate attribution.
