from tkinter import Tk, Label, Button, Frame, ttk, messagebox,filedialog, StringVar, LabelFrame
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os

class Student:
    def __init__(self, root):
        """Initialize the Student Management System window."""
        self.root = root
        self.root.geometry("1280x720+0+0")  # Adjusted for smaller screens
        self.root.title("Student Management System")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.var_dept = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_subject = StringVar()
        self.var_rollno = StringVar()
        self.var_semail = StringVar()
        self.var_radio1 = StringVar()

        # Title label
        title_lbl = Label(self.root, text="Student Management System", font=("Helvetica", 24, "bold"), 
                         fg="#2c3e50", bg="#f0f0f0")
        title_lbl.place(relx=0, rely=0, relwidth=1, height=50)

        # Main frame
        main_frame = Frame(self.root, bg="#e6e6e6")
        main_frame.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.90)
        main_frame.columnconfigure((0, 1), weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Left frame (Form)
        left_frame = LabelFrame(main_frame, bg="white", relief="ridge",
                               text="Student Details", font=("Helvetica", 12, "bold"), fg="#2c3e50",
                               padx=10, pady=10)
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Course Information frame
        course_frame = LabelFrame(left_frame, bg="white", relief="ridge",
                                 text="Course Information", font=("Helvetica", 12, "bold"), fg="#2c3e50")
        course_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Course fields
        fields = [
            ("Departments", self.var_dept, ["Select Department", "COE", "ENC", "Civil", "Mechanical"]),
            ("Year", self.var_year, ["Select Year", "UG1", "UG2", "UG3", "UG4", "PG1", "PG2"]),
            ("Semester", self.var_semester, ["Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]),
            ("Subject", self.var_subject, None)
        ]

        for i, (label_text, var, values) in enumerate(fields):
            label = Label(course_frame, text=label_text, font=("Helvetica", 12, "bold"), bg="white")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            if values:  # Combobox
                combo = ttk.Combobox(course_frame, textvariable=var, values=values,
                                    state="readonly", font=("Helvetica", 11))
                combo.current(0)
                combo.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            else:  # Entry
                entry = ttk.Entry(course_frame, textvariable=var, font=("Helvetica", 11))
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")

        # Student Data frame
        student_frame = LabelFrame(left_frame, bg="white", relief="ridge",
                                  text="Student Data", font=("Helvetica", 12, "bold"), fg="#2c3e50")
        student_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Student fields
        Label(student_frame, text="Roll No:", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(student_frame, textvariable=self.var_rollno, font=("Helvetica", 11)).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        Label(student_frame, text="Email:", font=("Helvetica", 12, "bold"), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(student_frame, textvariable=self.var_semail, font=("Helvetica", 11)).grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Radio buttons
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes").grid(row=2, column=0, pady=10)
        ttk.Radiobutton(student_frame, variable=self.var_radio1, text="No Photo Sample", value="No").grid(row=2, column=1, pady=10)

        # Buttons frame
        btn_frame = Frame(student_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        btn_frame.columnconfigure((0, 1, 2, 3), weight=1)

        buttons = [
            ("Save", self.add_data),
            ("Update", self.update_data),
            ("Delete", self.delete_data),
            ("Reset", self.reset_data),
            ("Take Photo Sample", self.generate_dataset),
            ("Update Photo Sample", lambda: None)  # Placeholder, no functionality provided
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = Button(btn_frame, text=text, command=cmd, font=("Helvetica", 12, "bold"),
                        bg="#3498db", fg="white", width=15, bd=0)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)

        # Right frame (Table)
        right_frame = LabelFrame(main_frame, bg="white", relief="ridge",
                                text="Student Details", font=("Helvetica", 12, "bold"), fg="#2c3e50",
                                padx=10, pady=10)
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Search frame
        search_frame = LabelFrame(right_frame, bg="white", relief="ridge",
                                 text="Search System", font=("Helvetica", 12, "bold"), fg="#2c3e50")
        search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        Label(search_frame, text="Search By:", font=("Helvetica", 12, "bold"), bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        search_combo = ttk.Combobox(search_frame, values=["Select", "Roll_No", "Phone_No", "Class"],
                                   state="readonly", font=("Helvetica", 11))
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        ttk.Entry(search_frame, font=("Helvetica", 11)).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        Button(search_frame, text="Search", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", width=10).grid(row=0, column=3, padx=5)
        Button(search_frame, text="Show All", font=("Helvetica", 12, "bold"), bg="#3498db", fg="white", width=10).grid(row=0, column=4, padx=5)

        # Table frame
        table_frame = Frame(right_frame, bg="white")
        table_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Scrollbars
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")

        # Treeview table
        self.student_table = ttk.Treeview(table_frame,
                                        columns=("dept", "rollno", "email", "year", "semester", "subject", "photo"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        # Table columns
        columns = [("dept", "Department"), ("rollno", "Roll No"), ("email", "Email"), ("year", "Year"),
                   ("semester", "Semester"), ("subject", "Subject"), ("photo", "PhotoSampleStatus")]
        for col, text in columns:
            self.student_table.heading(col, text=text)
            self.student_table.column(col, width=100)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill="both", expand=True)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    def add_data(self):
        """Add student data to the database."""
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                         database="facerecognition_att")
            my_cursor = conn.cursor()
            my_cursor.execute("INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                self.var_dept.get(), self.var_rollno.get(), self.var_semail.get(),
                self.var_year.get(), self.var_semester.get(), self.var_subject.get(), self.var_radio1.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Data Added Successfully!", parent=self.root)
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def fetch_data(self):
        """Fetch student data from the database and populate table."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                         database="facerecognition_att")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in data:
                self.student_table.insert("", "end", values=row)
            conn.commit()
            conn.close()
        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def get_cursor(self, event=""):
        """Populate form fields when a table row is clicked."""
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        if data:
            self.var_dept.set(data[0])
            self.var_rollno.set(data[1])
            self.var_semail.set(data[2])
            self.var_year.set(data[3])
            self.var_semester.set(data[4])
            self.var_subject.set(data[5])
            self.var_radio1.set(data[6])

    def update_data(self):
        """Update student data in the database."""
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        if messagebox.askyesno("Update", "Are you sure you want to update this student?", parent=self.root):
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                             database="facerecognition_att")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE student SET Dep=%s, email=%s, year=%s, semester=%s, subject=%s, photo=%s WHERE roll_no=%s",
                    (self.var_dept.get(), self.var_semail.get(), self.var_year.get(),
                     self.var_semester.get(), self.var_subject.get(), self.var_radio1.get(), self.var_rollno.get())
                )
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def delete_data(self):
        """Delete student data from the database."""
        if self.var_rollno.get() == "":
            messagebox.showerror("Error", "Roll No is required", parent=self.root)
            return
        if messagebox.askyesno("Delete", "Are you sure you want to delete this student?", parent=self.root):
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                             database="facerecognition_att")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM student WHERE roll_no=%s", (self.var_rollno.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Student details deleted successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def reset_data(self):
        """Clear all form fields."""
        self.var_dept.set("Select Department")
        self.var_rollno.set("")
        self.var_semail.set("")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_subject.set("")
        self.var_radio1.set("")

    def generate_dataset(self):
        """Capture student photos and save to 'data' directory."""
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return
        try:
            # Create 'data' directory if it doesn't exist
            os.makedirs("data", exist_ok=True)

            # Load face classifier
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            if face_classifier.empty():
                messagebox.showerror("Error", "Failed to load face classifier", parent=self.root)
                return

            def face_cropped(img):
                """Crop detected face from the image."""
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    return img[y:y+h, x:x+w]
                return None

            # Open webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Unable to access the camera", parent=self.root)
                return

            img_id = 0
            student_id = self.var_rollno.get()
            while True:
                ret, my_frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "Failed to capture image", parent=self.root)
                    break

                cropped_face = face_cropped(my_frame)
                if cropped_face is not None:
                    img_id += 1
                    face = cv2.resize(cropped_face, (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    file_name_path = f"data/user.{student_id}.{img_id}.jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                    cv2.imshow("Cropped Face", face)

                if cv2.waitKey(1) == 13 or img_id == 100:  # Exit on Enter or after 100 images
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Photo dataset generated successfully!", parent=self.root)

            # Update photo status in database
            conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                         database="facerecognition_att")
            my_cursor = conn.cursor()
            my_cursor.execute("UPDATE student SET photo=%s WHERE roll_no=%s",
                             (self.var_radio1.get(), self.var_rollno.get()))
            conn.commit()
            self.fetch_data()
            conn.close()

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()