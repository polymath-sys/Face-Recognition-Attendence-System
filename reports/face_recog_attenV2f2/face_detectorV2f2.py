from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import mysql.connector
import datetime


class FaceDetector:
    """
    Face detection and attendance marking system.
    Uses face recognition to identify students and mark attendance.
    """
    
    def __init__(self, root: Tk):
        """
        Initialize the face detection window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.geometry("1000x700+200+50")  # Adjusted size
        self.root.title("Face Detection")
        self.root.configure(bg="#f0f0f0")

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'v26qtE%$11',
            'database': 'facerecognition_att'
        }

        # UI Setup
        self._setup_ui()

        # Face recognition variables
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read("classifier/classifier.xml")
        except:
            messagebox.showwarning(
                "Warning",
                "Classifier not found. Please train the model first.",
                parent=self.root
            )

    def _setup_ui(self):
        """Setup the user interface components."""
        # Title Label
        title_lbl = Label(
            self.root,
            text="Face Detection for Attendance",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_lbl.pack(pady=10)

        # Video Frame
        self.video_frame = LabelFrame(
            self.root,
            text="Camera Feed",
            font=("Helvetica", 12),
            bg="white",
            fg="#2c3e50"
        )
        self.video_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)

        self.video_label = Label(self.video_frame, bg="white")
        self.video_label.pack(pady=10)

        # Controls Frame
        controls_frame = Frame(self.root, bg="#f0f0f0")
        controls_frame.pack(pady=10)

        # Start/Stop Buttons
        self.start_btn = Button(
            controls_frame,
            text="Start Detection",
            command=self._start_detection,
            font=("Helvetica", 12, "bold"),
            bg="#27ae60",
            fg="white",
            width=15,
            bd=0
        )
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = Button(
            controls_frame,
            text="Stop Detection",
            command=self._stop_detection,
            font=("Helvetica", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=15,
            bd=0,
            state=DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=10)

        # Status Label
        self.status_label = Label(
            self.root,
            text="Ready to detect faces",
            font=("Helvetica", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.status_label.pack(pady=10)

        # Initialize video capture
        self.vid = None
        self.detection_active = False

    def _start_detection(self):
        """Start the face detection process."""
        try:
            self.vid = cv2.VideoCapture(0)
            if not self.vid.isOpened():
                raise Exception("Could not open video device")

            self.detection_active = True
            self.start_btn.config(state=DISABLED)
            self.stop_btn.config(state=NORMAL)
            self.status_label.config(text="Detection active...", fg="#27ae60")
            self._detect_faces()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to start camera:\n{str(e)}",
                parent=self.root
            )

    def _stop_detection(self):
        """Stop the face detection process."""
        self.detection_active = False
        self.start_btn.config(state=NORMAL)
        self.stop_btn.config(state=DISABLED)
        self.status_label.config(text="Detection stopped", fg="#e74c3c")

        if self.vid is not None:
            self.vid.release()
            self.vid = None

        # Clear video frame
        self.video_label.config(image=None)

    def _detect_faces(self):
        """Perform face detection and recognition."""
        if not self.detection_active or self.vid is None:
            return

        ret, frame = self.vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_gray = cv2.resize(roi_gray, (200, 200))

                # Recognize face
                try:
                    id, confidence = self.recognizer.predict(roi_gray)
                    
                    if confidence < 70:  # Confidence threshold
                        student_info = self._get_student_info(id)
                        if student_info:
                            dept, roll, name = student_info
                            cv2.putText(
                                frame, f"{name} ({roll})",
                                (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.8, (255, 255, 255), 2
                            )
                            
                            # Mark attendance
                            self._mark_attendance(roll, dept)
                    else:
                        cv2.putText(
                            frame, "Unknown",
                            (x, y-10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (255, 255, 255), 2
                        )

                except Exception as e:
                    print(f"Recognition error: {str(e)}")

            # Display frame
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(image=img)
            
            self.video_label.img = img  # Keep reference
            self.video_label.config(image=img)

        # Continue detection
        self.video_label.after(10, self._detect_faces)

    def _get_student_info(self, roll_no: int):
        """
        Get student information from database.
        
        Args:
            roll_no: Student roll number
            
        Returns:
            Tuple of (department, roll_no, name) or None if not found
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT Dep, roll_no, email FROM student WHERE roll_no=%s",
                (roll_no,)
            )
            result = cursor.fetchone()
            
            if result:
                return (result[0], result[1], result[2])
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
        
        return None

    def _mark_attendance(self, roll_no: str, dept: str):
        """
        Mark attendance for recognized student.
        
        Args:
            roll_no: Student roll number
            dept: Student department
        """
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            current_date = datetime.datetime.now().strftime("%d-%m-%Y")
            
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check if attendance already marked today
            cursor.execute(
                "SELECT * FROM attendance WHERE roll_no=%s AND date=%s",
                (roll_no, current_date)
            )
            
            if cursor.fetchone() is None:
                # Insert new attendance record
                cursor.execute(
                    "INSERT INTO attendance (roll_no, department, year, date, time, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (roll_no, dept, "N/A", current_date, current_time, "Present")
                )
                conn.commit()
                
                self.status_label.config(
                    text=f"Attendance marked for {roll_no}",
                    fg="#27ae60"
                )
            else:
                self.status_label.config(
                    text=f"Attendance already marked for {roll_no} today",
                    fg="#f39c12"
                )
                
        except mysql.connector.Error as err:
            self.status_label.config(
                text=f"Error marking attendance: {err}",
                fg="#e74c3c"
            )
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def __del__(self):
        """Clean up resources when object is destroyed."""
        if hasattr(self, 'vid') and self.vid is not None:
            self.vid.release()


if __name__ == "__main__":
    root = Tk()
    app = FaceDetector(root)
    root.mainloop()