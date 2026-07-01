from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import numpy as np


class Student:
    """
    Student management system for face recognition attendance system.
    Handles student registration, photo capture, and database operations.
    """
    
    def __init__(self, root: Tk):
        """
        Initialize the student management window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.geometry("1200x680+50+50")  # Adjusted for smaller screens
        self.root.title("Student Management System")
        self.root.configure(bg="#f0f0f0")

        # Database configuration
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'v26qtE%$11',
            'database': 'facerecognition_att'
        }

        # Form variables
        self.var_dept = StringVar()
        self.var_roll = StringVar()
        self.var_email = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_subject = StringVar()
        self.var_photo_status = StringVar()

        self._setup_ui()
        self.fetch_data()

    def _setup_ui(self):
        """Setup all UI components."""
        # Title Label
        title_lbl = Label(
            self.root,
            text="Student Management System",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_lbl.place(x=0, y=10, relwidth=1, height=45)

        # Main Frame
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.place(x=10, y=60, width=1180, height=600)

        # Left Frame (Student Details)
        left_frame = LabelFrame(
            main_frame,
            text="Student Details",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        left_frame.place(x=10, y=10, width=570, height=580)

        self._setup_left_frame(left_frame)

        # Right Frame (Records)
        right_frame = LabelFrame(
            main_frame,
            text="Student Records",
            font=("Helvetica", 12, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        right_frame.place(x=590, y=10, width=570, height=580)

        self._setup_right_frame(right_frame)

    def _setup_left_frame(self, parent: Frame):
        """Setup the left frame with student details form."""
        # Course Information
        course_frame = LabelFrame(
            parent,
            text="Course Information",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        course_frame.place(x=10, y=10, width=550, height=200)

        # Department
        Label(
            course_frame, text="Department:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=0, column=0, padx=5, pady=5, sticky=W)

        dept_combo = ttk.Combobox(
            course_frame, textvariable=self.var_dept,
            values=["Select Department", "COE", "ENC", "Civil", "Mechanical"],
            state="readonly", font=("Helvetica", 10), width=22
        )
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Year
        Label(
            course_frame, text="Year:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=1, column=0, padx=5, pady=5, sticky=W)

        year_combo = ttk.Combobox(
            course_frame, textvariable=self.var_year,
            values=["Select Year", "UG1", "UG2", "UG3", "UG4", "PG1", "PG2"],
            state="readonly", font=("Helvetica", 10), width=22
        )
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Semester
        Label(
            course_frame, text="Semester:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=2, column=0, padx=5, pady=5, sticky=W)

        sem_combo = ttk.Combobox(
            course_frame, textvariable=self.var_semester,
            values=["Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"],
            state="readonly", font=("Helvetica", 10), width=22
        )
        sem_combo.current(0)
        sem_combo.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        # Subject
        Label(
            course_frame, text="Subject:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=3, column=0, padx=5, pady=5, sticky=W)

        ttk.Entry(
            course_frame, textvariable=self.var_subject,
            font=("Helvetica", 10), width=24
        ).grid(row=3, column=1, padx=5, pady=5, sticky=W)

        # Student Data
        student_frame = LabelFrame(
            parent,
            text="Student Data",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        student_frame.place(x=10, y=220, width=550, height=200)

        # Roll Number
        Label(
            student_frame, text="Roll No:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=0, column=0, padx=5, pady=5, sticky=W)

        ttk.Entry(
            student_frame, textvariable=self.var_roll,
            font=("Helvetica", 10), width=24
        ).grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Email
        Label(
            student_frame, text="Email:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=1, column=0, padx=5, pady=5, sticky=W)

        ttk.Entry(
            student_frame, textvariable=self.var_email,
            font=("Helvetica", 10), width=24
        ).grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Photo Sample
        Label(
            student_frame, text="Photo Sample:",
            font=("Helvetica", 11), bg="white"
        ).grid(row=2, column=0, padx=5, pady=5, sticky=W)

        ttk.Radiobutton(
            student_frame, text="Take Photo", variable=self.var_photo_status,
            value="Yes", style='Toolbutton'
        ).grid(row=2, column=1, padx=5, pady=5, sticky=W)

        ttk.Radiobutton(
            student_frame, text="No Photo", variable=self.var_photo_status,
            value="No", style='Toolbutton'
        ).grid(row=2, column=2, padx=5, pady=5, sticky=W)

        # Buttons Frame
        btn_frame = Frame(student_frame, bg="white")
        btn_frame.place(x=5, y=100, width=540, height=80)

        buttons = [
            ("Save", self.add_data),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("Reset", self.reset_data),
            ("Take Photo", self.generate_dataset)
        ]

        for col, (text, command) in enumerate(buttons[:4]):
            Button(
                btn_frame, text=text, command=command,
                font=("Helvetica", 10, "bold"),
                bg="#3498db", fg="white",
                width=12, height=1,
                bd=0, relief=FLAT
            ).grid(row=0, column=col, padx=5, pady=5)

        Button(
            btn_frame, text=buttons[4][0], command=buttons[4][1],
            font=("Helvetica", 10, "bold"),
            bg="#3498db", fg="white",
            width=25, height=1,
            bd=0, relief=FLAT
        ).grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    def _setup_right_frame(self, parent: Frame):
        """Setup the right frame with student records table."""
        # Search Frame
        search_frame = LabelFrame(
            parent,
            text="Search System",
            font=("Helvetica", 11, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        search_frame.place(x=5, y=10, width=560, height=80)

        # Search Combo
        search_combo = ttk.Combobox(
            search_frame,
            values=["Select", "Roll No", "Email", "Department"],
            state="readonly", font=("Helvetica", 10), width=15
        )
        search_combo.current(0)
        search_combo.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # Search Entry
        ttk.Entry(
            search_frame, font=("Helvetica", 10), width=18
        ).grid(row=0, column=1, padx=5, pady=5, sticky=W)

        # Search Buttons
        Button(
            search_frame, text="Search",
            font=("Helvetica", 10, "bold"),
            bg="#3498db", fg="white",
            width=10, bd=0
        ).grid(row=0, column=2, padx=5, pady=5)

        Button(
            search_frame, text="Show All",
            font=("Helvetica", 10, "bold"),
            bg="#3498db", fg="white",
            width=10, bd=0
        ).grid(row=0, column=3, padx=5, pady=5)

        # Table Frame
        table_frame = Frame(parent, bg="white")
        table_frame.place(x=5, y=100, width=560, height=450)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            table_frame,
            columns=("dept", "roll", "email", "year", "semester", "subject", "photo"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Configure table headings
        columns = {
            "dept": "Department",
            "roll": "Roll No",
            "email": "Email",
            "year": "Year",
            "semester": "Semester",
            "subject": "Subject",
            "photo": "Photo Status"
        }

        for col, text in columns.items():
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=100)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

    # Database Operations
    def add_data(self):
        """Add new student record to the database."""
        if (self.var_dept.get() == "Select Department" or 
            self.var_roll.get() == "" or
            self.var_email.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = """
            INSERT INTO student 
            (Dep, roll_no, email, year, semester, subject, photo) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                self.var_dept.get(),
                self.var_roll.get(),
                self.var_email.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_subject.get(),
                self.var_photo_status.get()
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Student added successfully", parent=self.root)
            self.fetch_data()
            self.reset_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}", parent=self.root)
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def fetch_data(self):
        """Fetch all student records from the database."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM student")
            rows = cursor.fetchall()
            
            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    self.student_table.insert("", END, values=row)
                    
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}", parent=self.root)
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def get_cursor(self, event):
        """Get selected row data and populate form fields."""
        cursor_row = self.student_table.focus()
        content = self.student_table.item(cursor_row)
        row = content["values"]
        
        if row:
            self.var_dept.set(row[0])
            self.var_roll.set(row[1])
            self.var_email.set(row[2])
            self.var_year.set(row[3])
            self.var_semester.set(row[4])
            self.var_subject.set(row[5])
            self.var_photo_status.set(row[6])

    def update_data(self):
        """Update selected student record."""
        if (self.var_dept.get() == "Select Department" or 
            self.var_roll.get() == ""):
            messagebox.showerror("Error", "Select a student to update", parent=self.root)
            return

        if not messagebox.askyesno("Confirm", "Update this student?", parent=self.root):
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            query = """
            UPDATE student SET 
            Dep=%s, email=%s, year=%s, semester=%s, subject=%s, photo=%s 
            WHERE roll_no=%s
            """
            
            values = (
                self.var_dept.get(),
                self.var_email.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_subject.get(),
                self.var_photo_status.get(),
                self.var_roll.get()
            )
            
            cursor.execute(query, values)
            conn.commit()
            
            messagebox.showinfo("Success", "Student updated successfully", parent=self.root)
            self.fetch_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}", parent=self.root)
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def delete_data(self):
        """Delete selected student record."""
        if self.var_roll.get() == "":
            messagebox.showerror("Error", "Select a student to delete", parent=self.root)
            return

        if not messagebox.askyesno("Confirm", "Delete this student?", parent=self.root):
            return

        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM student WHERE roll_no=%s", (self.var_roll.get(),))
            conn.commit()
            
            messagebox.showinfo("Success", "Student deleted successfully", parent=self.root)
            self.fetch_data()
            self.reset_data()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}", parent=self.root)
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def reset_data(self):
        """Reset all form fields to default values."""
        self.var_dept.set("Select Department")
        self.var_roll.set("")
        self.var_email.set("")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_subject.set("")
        self.var_photo_status.set("")

    def generate_dataset(self):
        """Capture face images for training dataset."""
        if (self.var_dept.get() == "Select Department" or 
            self.var_roll.get() == ""):
            messagebox.showerror("Error", "Department and Roll No are required", parent=self.root)
            return

        try:
            # Create data directory if not exists
            if not os.path.exists("data"):
                os.makedirs("data")

            # Load face detection classifier
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            # Initialize webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise Exception("Could not open video device")

            img_count = 0
            student_id = self.var_roll.get()

            while img_count < 100:  # Capture 100 images
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Failed to capture frame")

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    img_count += 1
                    
                    # Save the face image
                    face_img = gray[y:y+h, x:x+w]
                    face_img = cv2.resize(face_img, (450, 450))
                    
                    img_path = f"data/user.{student_id}.{img_count}.jpg"
                    cv2.imwrite(img_path, face_img)
                    
                    cv2.putText(
                        frame, f"Images: {img_count}", 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 0), 2
                    )

                cv2.imshow("Face Capture", frame)
                
                if cv2.waitKey(1) == 13 or img_count >= 100:  # Exit on ENTER key
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Update photo status in database
            self.var_photo_status.set("Yes")
            self.update_data()
            
            messagebox.showinfo(
                "Success", 
                f"Dataset generated successfully with {img_count} images",
                parent=self.root
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate dataset: {str(e)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()