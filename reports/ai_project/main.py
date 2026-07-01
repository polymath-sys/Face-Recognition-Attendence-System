from tkinter import Tk, Label, Button, Frame, Toplevel
from PIL import Image, ImageTk
from studentV2f3 import Student
from trainV2f3 import Train
from face_detectorV2f3 import Face_Detector
from attendenceV2f3 import Attendance
import os

class Face_Recognition_System:
    def __init__(self, root):
        """Initialize the main Face Recognition System window."""
        self.root = root
        self.root.geometry("1280x720+0+0")  # Adjusted for smaller screens
        self.root.title("Face Recognition System")
        self.root.configure(bg="#f0f0f0")  # Light background for clean look

        # Load and resize background image
        img = Image.open(r"assets\bg.png")
        img = img.resize((600, 150), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)

        # Place background image
        bg_label = Label(self.root, image=self.bg_image, bg="#f0f0f0")
        bg_label.place(relx=0.5, rely=0.85, anchor="center")

        # Title label
        title_lbl = Label(self.root, text="Face Recognition Attendance System\nMade By", 
                         font=("Helvetica", 24, "bold"), fg="#2c3e50", bg="#f0f0f0")
        title_lbl.place(relx=0.5, rely=0.2, anchor="center")

        # Names label
        names_lbl = Label(self.root, 
                         text="Aditya Pandey (102303968)\nYash Vardhan Singh (102303725)\nMehul Kujur (102303712)", 
                         font=("Helvetica", 16), fg="#2c3e50", bg="#f0f0f0")
        names_lbl.place(relx=0.5, rely=0.35, anchor="center")

        # Button frame for responsive layout
        btn_frame = Frame(self.root, bg="#f0f0f0")
        btn_frame.place(relx=0.5, rely=0.55, anchor="center")

        # Configure grid for buttons
        btn_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)
        btn_frame.rowconfigure(0, weight=1)

        # Buttons with consistent styling
        buttons = [
            ("Student", self.student_details),
            ("Detect Face", self.detect_face),
            ("Attendance", self.attendance_data),
            ("Train Face", self.train_data),
            ("Photos", self.open_img)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = Button(btn_frame, text=text, command=cmd, cursor="hand2", 
                        font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", 
                        width=12, height=2, bd=0)
            btn.grid(row=0, column=i, padx=10, pady=10)

    def open_img(self):
        """Open the 'data' directory to view photos."""
        os.startfile("data")

    def student_details(self):
        """Open the Student management window."""
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        """Open the Train dataset window."""
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def detect_face(self):
        """Open the Face Detector window."""
        self.new_window = Toplevel(self.root)
        self.app = Face_Detector(self.new_window)

    def attendance_data(self):
        """Open the Attendance management window."""
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()