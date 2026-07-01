# Face Recognition Attendance System

This project is a Tkinter-based desktop application for managing student records, capturing face samples, training an LBPH face recognizer, and marking attendance from a webcam.

The active application is built around four main flows:

1. Maintain student details in MySQL.
2. Capture face images for each student.
3. Train a face-recognition model from the saved images.
4. Detect a face from the webcam and write attendance to CSV.

## Main Screens

- `main.py` opens the home window and acts as the launcher for the other modules.
- `studentV2f.py` manages student records and face-sample capture.
- `trainV2f.py` trains the recognizer from saved face images.
- `face_detectorV2f.py` runs live recognition and records attendance.
- `attendenceV2f.py` provides a CSV-based attendance viewer/editor.

## Project Workflow

### 1. Add student details

The Student window stores metadata such as department, roll number, email, year, semester, subject, and photo-sample status in MySQL.

### 2. Capture face samples

From the Student window, the app can open the webcam and save up to 100 grayscale face crops per student in the `data/` folder.

Saved images use the naming pattern:

`data/user.<roll_no>.<image_id>.jpg`

### 3. Train the model

The Train window reads all images in `data/`, extracts the student ID from the filename, trains an OpenCV LBPH recognizer, and writes the model to:

`classifier/classifier.xml`

### 4. Detect faces and mark attendance

The Face Detector window opens the webcam, detects faces with OpenCV Haar cascades, compares them against the trained model, and appends attendance rows to:

`attSheet.csv`

### 5. Review attendance

The Attendance window can import and export CSV files and display attendance data in a table.

## Data Files and Folders

- `assets/` - UI images used by the home screen.
- `data/` - saved face samples for training.
- `classifier/` - the trained LBPH model output.
- `attSheet.csv` - attendance log written by face detection.
- `haarcascade_frontalface_default.xml` - Haar cascade file included in the project root.

## Database Expectations

The code expects a local MySQL database named `facerecognition_att` with a `student` table.

The repository includes `database_setup.sql` for creating the database and table, and `config.ini` for local MySQL settings.

The Student module reads and writes fields that correspond to:

- department
- roll number
- email
- year
- semester
- subject
- photo sample status

The Face Detector module looks up student information by roll number when a face is recognized.

## Dependencies

The application uses:

- Python 3
- Tkinter
- Pillow
- OpenCV (`cv2`)
- OpenCV contrib modules for `cv2.face`
- NumPy
- MySQL Connector/Python

## How to Run

1. Install Python 3.
2. Create a virtual environment if you want to isolate dependencies.
3. Install the packages from `requirements.txt`.
4. Run `database_setup.sql` in MySQL.
5. Edit `config.ini` if your MySQL username, password, or database name are different.
6. Run `main.py`.

For a more detailed step-by-step guide, see [SETUP.md](SETUP.md).

If you want to contribute or extend the project, see [CONTRIBUTING.md](CONTRIBUTING.md).

The main window provides buttons for Student management, face detection, training, and attendance review.

## File-by-File Summary

### `main.py`

Launches the application home screen and opens each module in a separate `Toplevel` window.

### `studentV2f.py`

Handles student CRUD operations, sample capture, and database synchronization.

### `trainV2f.py`

Reads saved face images and trains the LBPH classifier.

### `face_detectorV2f.py`

Captures webcam frames, detects faces, predicts identities, and writes attendance entries.

### `attendenceV2f.py`

Loads and saves attendance CSV files and shows them in a table.

## Notes

- The code contains older or commented-out versions of some windows in a few files. The active implementation is the one imported and launched from `main.py`.
- The MySQL settings are read from `config.ini`, so update that file for your local environment.
- The attendance flow assumes a working webcam and a trained classifier in `classifier/classifier.xml`.

## Typical Usage Order

1. Open the Student window and add a student.
2. Capture face samples for that student.
3. Train the model.
4. Open Face Detector to recognize faces and write attendance.
5. Use Attendance to inspect or export the CSV log.