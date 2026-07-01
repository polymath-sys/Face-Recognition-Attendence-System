from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from studentV2f2 import Student
import os
from trainV2f2 import Train
from face_detectorV2f2 import FaceDetector
from attendenceV2f2 import Attendance


class FaceRecognitionSystem:
    """
    Main application window for the Face Recognition Attendance System.
    Provides navigation to all system features.
    """
    
    def __init__(self, root: Tk):
        """
        Initialize the main application window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.geometry("1200x700+50+50")  # Adjusted for smaller screens
        self.root.title("Face Recognition System")
        self.root.configure(bg="#f0f0f0")

        self._setup_ui()

    def _setup_ui(self):
        """Setup the main application UI components."""
        # Title Label
        title_lbl = Label(
            self.root, 
            text="Face Recognition Attendance System",
            font=("Helvetica", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_lbl.place(x=0, y=50, relwidth=1, height=60)

        # Developers Label
        devs_lbl = Label(
            self.root,
            text="Developed By:\nAditya Pandey, Yash Vardhan Singh, Mehul Kujur",
            font=("Helvetica", 14),
            fg="#34495e",
            bg="#f0f0f0"
        )
        devs_lbl.place(x=0, y=120, relwidth=1, height=80)

        # Buttons Frame
        btn_frame = Frame(self.root, bg="#f0f0f0")
        btn_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=800, height=100)

        # Navigation Buttons
        buttons = [
            ("Student", self.student_details),
            ("Detect Face", self.detect_face),
            ("Attendance", self.attendance_data),
            ("Train Face", self.train_data),
            ("Photos", self.open_img)
        ]

        for idx, (text, command) in enumerate(buttons):
            Button(
                btn_frame, text=text, command=command,
                font=("Helvetica", 12, "bold"),
                bg="#3498db", fg="white",
                width=12, height=2,
                bd=0, relief=FLAT,
                activebackground="#2980b9"
            ).grid(row=0, column=idx, padx=10, pady=10)

    def open_img(self):
        """Open the data directory containing student photos."""
        try:
            os.startfile("data")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {str(e)}")

    def student_details(self):
        """Open the student management window."""
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        """Open the face training window."""
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def detect_face(self):
        """Open the face detection window."""
        self.new_window = Toplevel(self.root)
        self.app = FaceDetector(self.new_window)

    def attendance_data(self):
        """Open the attendance management window."""
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)


if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionSystem(root)
    root.mainloop()