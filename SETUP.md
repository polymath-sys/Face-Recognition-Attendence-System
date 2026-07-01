# Setup Guide

This guide explains how to set up and run the project on a Windows device after downloading it from GitHub.

## Prerequisites

- Windows 10 or later
- Python 3.10+ installed and added to PATH
- MySQL Server installed and running
- A webcam for face capture and detection

## 1. Open the Project Folder

Open the downloaded repository folder in File Explorer or VS Code.

The main application entry point is [main.py](main.py).

## 2. Create a Virtual Environment

Open PowerShell in the project folder and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## 3. Install Python Dependencies

Install the packages listed in [requirements.txt](requirements.txt):

```powershell
pip install -r requirements.txt
```

The project depends on:

- Pillow
- OpenCV Contrib
- NumPy
- MySQL Connector/Python

## 4. Create the MySQL Database

Open MySQL Workbench, phpMyAdmin, or the MySQL command line and run [database_setup.sql](database_setup.sql).

That script creates:

- the `facerecognition_att` database
- the `student` table used by the Student and Face Detector windows

## 5. Configure Local Database Access

Edit [config.ini](config.ini) if your local MySQL settings are different.

Example:

```ini
[mysql]
host = localhost
username = root
password = your_password_here
database = facerecognition_att
```

## 6. Run the App

Start the application from the project root:

```powershell
python main.py
```

## 7. Use the App in the Correct Order

1. Open Student and add a student record.
2. Capture face samples for that student.
3. Open Train Face and train the classifier.
4. Open Detect Face to recognize faces and write attendance.
5. Open Attendance to inspect or export the CSV log.

## Common Output Files

- `data/` stores captured face samples.
- `classifier/classifier.xml` stores the trained LBPH model.
- `attSheet.csv` stores attendance rows.

## Troubleshooting

- If `cv2.face` is missing, install `opencv-contrib-python` instead of base OpenCV.
- If MySQL errors appear, confirm the database exists and `config.ini` matches your local credentials.
- If the webcam does not open, close other apps using the camera and try again.