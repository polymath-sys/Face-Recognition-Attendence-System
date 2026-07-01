from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os
from db_config import get_db_connection

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Student Management System")

        # ============ Variables ==========
        self.var_dept = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_subject = StringVar()
        self.var_rollno = StringVar()
        self.var_semail = StringVar()
        self.var_radio1 = StringVar()

        # Title Label
        title_lbl = Label(self.root, text="Student Management System", font=("", 30, "bold"), fg="brown")
        title_lbl.place(x=0, y=0, width=1750, height=50)

        # Main Frame
        main_frame = Frame(self.root, bd=2)
        main_frame.place(x=10, y=51, width=1750, height=780)

        # Left Label Frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                font=(" ", 12, "bold"), fg="brown")
        left_frame.place(x=0, y=0, width=825, height=780)

        # Course Information Frame
        course_details_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Course Information",
                                         font=(" ", 12, "bold"), fg="brown")
        course_details_frame.place(x=0, y=20, width=820, height=300)

        # Department
        dept_label = Label(course_details_frame, text="Departments", font=(" ", 12, "bold"))
        dept_label.grid(row=0, column=0, padx=10, sticky=W)

        dept_combo = ttk.Combobox(course_details_frame, textvariable=self.var_dept, font=(" ", 12, "bold"),
                                  state="readonly")
        dept_combo["values"] = ("Select Department", "COE", "ENC", "Civil", "Mechanical")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(course_details_frame, text="Year", font=(" ", 12, "bold"))
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(course_details_frame, textvariable=self.var_year, font=(" ", 12, "bold"),
                                  state="readonly")
        year_combo["values"] = ("Select Year", "UG1", "UG2", "UG3", "UG4", "PG1", "PG2")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        sem_label = Label(course_details_frame, text="Semester", font=(" ", 12, "bold"))
        sem_label.grid(row=2, column=0, padx=10, sticky=W)

        sem_combo = ttk.Combobox(course_details_frame, textvariable=self.var_semester, font=(" ", 12, "bold"),
                                 state="readonly")
        sem_combo["values"] = ("Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        sem_combo.current(0)
        sem_combo.grid(row=2, column=1, padx=2, pady=10, sticky=W)

        # Subject
        subject_label = Label(course_details_frame, text="Subject", font=(" ", 12, "bold"))
        subject_label.grid(row=3, column=0, padx=10, sticky=W)

        sub_entry = ttk.Entry(course_details_frame, textvariable=self.var_subject, width=20, font=(" ", 13, "bold"))
        sub_entry.grid(row=3, column=1, padx=10, sticky=W)

        # Student Data Frame
        student_data_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Student Data",
                                       font=(" ", 12, "bold"), fg="brown")
        student_data_frame.place(x=0, y=330, width=820, height=450)

        # Roll No
        rollno_label = Label(student_data_frame, text="Roll No:", font=(" ", 12, "bold"))
        rollno_label.grid(row=0, column=0, padx=10, sticky=W)

        rollno_entry = ttk.Entry(student_data_frame, textvariable=self.var_rollno, width=20, font=(" ", 13, "bold"))
        rollno_entry.grid(row=0, column=1, padx=10, sticky=W)

        # Email
        semail_label = Label(student_data_frame, text="Email:", font=(" ", 12, "bold"))
        semail_label.grid(row=1, column=0, padx=10, sticky=W)

        semail_entry = ttk.Entry(student_data_frame, textvariable=self.var_semail, width=20, font=(" ", 13, "bold"))
        semail_entry.grid(row=1, column=1, padx=10, sticky=W)

        # Radio Buttons
        radiob1 = ttk.Radiobutton(student_data_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radiob1.grid(row=5, column=0)

        radiob2 = ttk.Radiobutton(student_data_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radiob2.grid(row=5, column=1)

        # Buttons Frame
        btn_frame = Frame(student_data_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=100, width=810, height=100)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=15, font=(" ", 13, "bold"),
                          bg="grey", fg="black")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=15, font=(" ", 13, "bold"),
                            bg="grey", fg="black")
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=15, font=(" ", 13, "bold"),
                            bg="grey", fg="black")
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=15, font=(" ", 13, "bold"),
                           bg="grey", fg="black")
        reset_btn.grid(row=0, column=3)

        take_photo_sample_btn = Button(btn_frame, text="Take Photo Sample", command=self.generate_dataset,
                                      width=17, font=(" ", 13, "bold"), bg="grey", fg="black")
        take_photo_sample_btn.grid(row=1, column=0)

        update_photo_sample_btn = Button(btn_frame, text="Update Photo Sample", width=17, font=(" ", 13, "bold"),
                                        bg="grey", fg="black")
        update_photo_sample_btn.grid(row=1, column=1)

        # Right Label Frame
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                 font=(" ", 12, "bold"), fg="brown")
        right_frame.place(x=850, y=0, width=850, height=780)

        # Search Frame
        search_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Search System",
                                  font=(" ", 12, "bold"), fg="brown")
        search_frame.place(x=0, y=20, width=840, height=100)

        search_label = Label(search_frame, text="Search By:", font=(" ", 15, "bold"))
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, font=(" ", 12, "bold"), state="readonly")
        search_combo["values"] = ("Select", "Roll_No", "Phone_No", "Class")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(search_frame, width=17, font=(" ", 13))
        search_entry.grid(row=0, column=2, padx=10, sticky=W)

        search_btn = Button(search_frame, text="Search", width=10, font=(" ", 13, "bold"), bg="grey", fg="black")
        search_btn.grid(row=0, column=3, padx=2)

        showAll_btn = Button(search_frame, text="Show All", width=10, font=(" ", 13, "bold"), bg="grey", fg="black")
        showAll_btn.grid(row=0, column=4)

        # Table Frame
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=0, y=110, width=840, height=400)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame,
                                         column=("dept", "rollno", "email", "year", "semester", "subject", "photo"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("rollno", text="Roll No")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("dept", text="Department")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("semester", text="Semester")
        self.student_table.heading("subject", text="Subject")
        self.student_table.heading("photo", text="PhotoSampleStatus")

        self.student_table.column("rollno", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("dept", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("semester", width=100)
        self.student_table.column("subject", width=100)
        self.student_table.column("photo", width=100)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    # ============ Functions ===========

    def add_data(self):
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                conn = get_db_connection()
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO student VALUES (%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_dept.get(),
                    self.var_rollno.get(),
                    self.var_semail.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_subject.get(),
                    self.var_radio1.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Data Added Successfully!", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = get_db_connection()
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM student")
        data = my_cursor.fetchall()

        if len(data) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
        conn.commit()
        conn.close()

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_dept.set(data[0])
        self.var_rollno.set(data[1])
        self.var_semail.set(data[2])
        self.var_year.set(data[3])
        self.var_semester.set(data[4])
        self.var_subject.set(data[5])
        self.var_radio1.set(data[6])

    def update_data(self):
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update", "Are you sure you want to update this student?", parent=self.root)
                if Update:
                    conn = get_db_connection()
                    my_cursor = conn.cursor()
                    my_cursor.execute(
                        "UPDATE student SET Dep=%s, email=%s, year=%s, semester=%s, subject=%s, photo=%s WHERE roll_no=%s",
                        (
                            self.var_dept.get(),
                            self.var_semail.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_subject.get(),
                            self.var_radio1.get(),
                            self.var_rollno.get()
                        ))
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Student details updated successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def delete_data(self):
        if self.var_rollno.get() == "":
            messagebox.showerror("Error", "Roll No is required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Delete", "Are you sure you want to delete this student?", parent=self.root)
                if delete:
                    conn = get_db_connection()
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM student WHERE roll_no=%s"
                    val = (self.var_rollno.get(),)
                    my_cursor.execute(sql, val)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    messagebox.showinfo("Success", "Student details deleted successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_dept.set("Select Department")
        self.var_rollno.set("")
        self.var_semail.set("")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_subject.set("")
        self.var_radio1.set("")

    def generate_dataset(self):
        if self.var_dept.get() == "Select Department" or self.var_rollno.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
            return

        try:
            # Ensure the 'data' directory exists
            if not os.path.exists("data"):
                os.makedirs("data")

            # Load face classifier
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            if face_classifier.empty():
                messagebox.showerror("Error", "Failed to load face classifier", parent=self.root)
                return

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    face_cropped = img[y:y+h, x:x+w]
                    return face_cropped
                return None

            # Open webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Unable to access the camera", parent=self.root)
                return

            img_id = 0
            student_id = self.var_rollno.get()  # Use roll number as ID
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

                if cv2.waitKey(1) == 13 or img_id == 100:  # Exit on 'Enter' key or after 100 images
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Success", "Photo dataset generated successfully!", parent=self.root)

            # Update photo status in database
            conn = get_db_connection()
            my_cursor = conn.cursor()
            my_cursor.execute(
                "UPDATE student SET photo=%s WHERE roll_no=%s",
                (self.var_radio1.get(), self.var_rollno.get())
            )
            conn.commit()
            self.fetch_data()
            conn.close()

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

            


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()