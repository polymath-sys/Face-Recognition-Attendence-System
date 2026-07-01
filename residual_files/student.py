from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os

class Student:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Student")

         #============Variables==========#
        self.var_dept = StringVar()
        self.var_year = StringVar()
        self.var_semester= StringVar()
        self.var_subject = StringVar()
        #

        self.var_rollno = StringVar()
        self.var_semail = StringVar()


        title_lbl = Label(text="Student Window lol", font=("",30,"bold"), fg="brown")
        title_lbl.place(x=0, y=0, width=1750, height=50)

        main_frame =  Frame(root,bd=2)
        main_frame.place(x=10,y=51,width=1750, height=780)

        #left Label Frame

        left_frame = LabelFrame(main_frame, bd=2,bg="white",relief=RIDGE, text="Student Details", 
                                font=(" ",12, "bold"),fg="brown")
        left_frame.place(x=0,y=0, width=825, height =780)

        #course information
        course_details_frame = LabelFrame(left_frame, bd=2,bg="white",relief=RIDGE, text="Course Information", font=(" ",12, "bold"),fg="brown")
        course_details_frame.place(x=0,y=20, width=820, height =300)

        #department
        dept_label = Label(course_details_frame, text="Departments", font=(" ",12,"bold"))
        dept_label.grid(row=0, column=0)

        dept_combo=ttk.Combobox(course_details_frame,textvariable=self.var_dept, font=(" ", 12, "bold"), state="readonly")
        dept_combo["values"]=("select department", "COE", "ENC", "Civil", "Mechnical")
        dept_combo.current(0)
        dept_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        #year
        year_label = Label(course_details_frame, text="Year", font=(" ",12,"bold"))
        year_label.grid(row=1, column=0, padx=10,sticky=W)

        year_combo=ttk.Combobox(course_details_frame,textvariable=self.var_year, font=(" ", 12, "bold"), state="readonly")
        year_combo["values"]=("select year","UG1", "UG2", "UG3", "UG4", "PG1", "PG2")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        #semester
        sem_label = Label(course_details_frame, text="Semester", font=(" ",12,"bold"))
        sem_label.grid(row=2, column=0, padx=10,sticky=W)

        sem_combo=ttk.Combobox(course_details_frame,textvariable=self.var_semester, font=(" ", 12, "bold"), state="readonly")
        sem_combo["values"]=("select semester","1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
        sem_combo.current(0)
        sem_combo.grid(row=2, column=1, padx=2, pady=10, sticky=W)

        #subject
        subject_label = Label(course_details_frame, text="Subject", font=(" ",12,"bold"))
        subject_label.grid(row=3, column=0, padx=10,sticky=W)

        sub_entry= ttk.Entry(course_details_frame,textvariable=self.var_subject, width= 20, font=(" ",13, "bold"))
        sub_entry.grid(row=3, column= 1, padx=10, sticky=W)

        #STUEDENT DATA  
        student_data_frame = LabelFrame(left_frame, bd=2,bg="white",relief=RIDGE, text="Student Data", font=(" ",12, "bold"),fg="brown")
        student_data_frame.place(x=0,y=330, width=820, height =550)

        #student id
        rollno_label = Label(student_data_frame, text="Roll No:", font=(" ",12,"bold"))
        rollno_label.grid(row=0, column=0, padx=10,sticky=W)

        rollno_entry= ttk.Entry(student_data_frame,textvariable=self.var_rollno, width= 20, font=(" ",13, "bold"))
        rollno_entry.grid(row=0, column= 1, padx=10, sticky=W)

        #student email
        semail_label = Label(student_data_frame, text="Email:", font=(" ",12,"bold"))
        semail_label.grid(row=1, column=0, padx=10,sticky=W)

        semail_entry= ttk.Entry(student_data_frame,textvariable=self.var_semail, width= 20, font=(" ",13, "bold"))
        semail_entry.grid(row=1, column= 1, padx=10, sticky=W)
        
        #RADIO BUTTONS
        self.var_radio1 = StringVar()
        radiob1 = ttk.Radiobutton(student_data_frame,variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radiob1.grid(row=5, column=0)

        # self.var_radio2 = StringVar()
        radiob2 = ttk.Radiobutton(student_data_frame,variable=self.var_radio1, text="No Photo Sample", value="No")
        radiob2.grid(row=5, column=1)

        #buttons frame
        btn_frame=Frame(student_data_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=100, width=810, height=100)
        
        save_btn=Button(btn_frame, text="Save",command=self.add_data, width=15,font=(" ",13,"bold"), bg= "grey",fg="black")
        save_btn.grid(row=0, column=0)

        update_btn=Button(btn_frame, text="Update",command=self.update_data,width=15,font=(" ",13,"bold"), bg= "grey",fg="black")
        update_btn.grid(row=0, column=1)

        delete_btn=Button(btn_frame, text="Delete",command=self.delete_data, width=15,font=(" ",13,"bold"), bg= "grey",fg="black")
        delete_btn.grid(row=0, column=2)

        reset_btn=Button(btn_frame, text="Reset", command=self.reset_data,width=15,font=(" ",13,"bold"), bg= "grey",fg="black")
        reset_btn.grid(row=0, column=3)

        take_photo_sample_btn=Button(btn_frame, text="Take Photo Sample", command=self.generate_dataset,width=17,font=(" ",13,"bold"), bg= "grey",fg="black")
        take_photo_sample_btn.grid(row=1, column=0)

        update_photo_sample_btn=Button(btn_frame, text="Update Photo Sample",width=17,font=(" ",13,"bold"), bg= "grey",fg="black")
        update_photo_sample_btn.grid(row=1, column=1)


        #right label frame
        right_frame = LabelFrame(main_frame, bd=2,bg="white",relief=RIDGE, text="Student Details",
                                 font=(" ",12, "bold"),fg="brown")
        right_frame.place(x=850,y=0, width=850, height =780)

        search_frame = LabelFrame(right_frame, bd=2,bg="white",relief=RIDGE, text="Search System", font=(" ",12, "bold"),fg="brown")
        search_frame.place(x=0,y=20, width=840, height =100)

        search_label = Label(search_frame, text="Search By:", font=(" ",15,"bold"))
        search_label.grid(row=0, column=0, padx=10, pady=5,sticky=W)

        
        search_combo=ttk.Combobox(search_frame, font=(" ", 12, "bold"), state="readonly")
        search_combo["values"]=("select", "Roll_No", "Phone_No", "Class")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry= ttk.Entry(search_frame, width= 17, font=(" ",13, ))
        search_entry.grid(row=0, column= 2, padx=10, sticky=W)
        
        search_btn=Button(search_frame, text="Search",width=10,font=(" ",13,"bold"), bg= "grey",fg="black")
        search_btn.grid(row=0, column=3, padx=2)

        showAll_btn=Button(search_frame, text="Show All",width=10,font=(" ",13,"bold"), bg= "grey",fg="black")
        showAll_btn.grid(row=0, column=4)

        #table frame
        table_frame = Frame(right_frame, bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=0,y=110, width=840, height =400)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, column=("dept","rollno","email","year","semester","subject", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
         
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

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
        
        self.student_table["show"]="headings"

        self.student_table.pack(fill=BOTH, expand=1)

        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

#==============FUNCTIONS===========#
    def add_data(self):
        if self.var_dept.get()=="Select Department" or self.var_rollno.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11", database="facerecognition_att")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s)",(
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
        
    
#=========Function to fetch data from database============#
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11", database="facerecognition_att")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        if len(data) !=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("", END, values=i)
                conn.commit()
        conn.close()

#===================get cursor=====================
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_dept.set(data[0]),
        self.var_rollno.set(data[1]),
        self.var_semail.set(data[2]),
        self.var_year.set(data[3]),
        self.var_semester.set(data[4]),
        self.var_subject.set(data[5]),
        self.var_radio1.set(data[6])

    #update function
    def update_data(self):
        if self.var_dept.get()=="Select Department" or self.var_rollno.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("update", "Pakka update krni hai, soch lo !?", parent=self.root)
                if Update:
                    conn=mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11", database="facerecognition_att")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set Dep=%s,email=%s,year=%s,semester=%s,subject=%s,photo=%s where roll_no=%s",(
                                                                                                                            self.var_dept.get(),
                                                                                                                           
                                                                                                                            self.var_semail.get(),
                                                                                                                            self.var_year.get(),
                                                                                                                            self.var_semester.get(),
                                                                                                                            self.var_subject.get(),
                                                                                                                            self.var_radio1.get(),
                                                                                                                            self.var_rollno.get(),
                                                                                                                            
                                                                                                                        ) )       
                    messagebox.showinfo("Success", "Hogya Update", parent = self.root)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent = self.root)

    #========DELETE FUNCTION==========

    def delete_data(self):
        if self.var_rollno.get()=="":
            messagebox.showerror("Error", "Roll No is required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("student delete page", "pakka delete karna hai iss student ko?", parent=self.root)
                if delete > 0:
                    conn=mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11", database="facerecognition_att")
                    my_cursor = conn.cursor()

                    sql="delete from student where roll_no =%s"
                    val=(self.var_rollno.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete", "successfully deleted student details")

            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent = self.root)


    #=============RESET BUTTON================#
    def reset_data(self):
        self.var_dept.set("select department"),
        self.var_rollno.set(""),
        self.var_semail.set(""),
        self.var_year.set("select year"),
        self.var_semester.set("select semester"),
        self.var_subject.set(""),
        self.var_radio1.set("")


#====================GENERATE DATA SET=========================#
    def generate_dataset(self):
        def update_data(self):
            if self.var_dept.get()=="Select Department" or self.var_rollno.get()=="":
                messagebox.showerror("Error","All Fields are required",parent=self.root)
            else:
                try:
                    conn=mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11", database="facerecognition_att")
                    my_cursor = conn.cursor()
                    my_cursor.execute("select * from student")
                    myresult = my_cursor.fetchall()

                    id =0
                    for x in myresult:
                        id += 1
                    my_cursor.execute("update student set Dep=%s,email=%s,year=%s,semester=%s,subject=%s,photo=%s where roll_no=%s",(
                                                                                                                                self.var_dept.get(),
                                                                                                                            
                                                                                                                                self.var_semail.get(),
                                                                                                                                self.var_year.get(),
                                                                                                                                self.var_semester.get(),
                                                                                                                                self.var_subject.get(),
                                                                                                                                self.var_radio1.get(),
                                                                                                                                self.var_rollno.get() == id+1
                                                                                                                                
                                                                                                                            ) ) 
                    conn.commit()
                    self.fecth_data()
                    self.reset_data()
                    conn.close()
                    
                    #============== Load predefined data on face frontals from opencv========

                    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                    def face_cropped(img):
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_classifier.detectMultiscale(gray, 1.3,5)
                        #scaling factor = 1.3
                        #minimum neigbor = 5
                        
                        for(x,y,w,h) in faces:
                            face_cropeed = img[y:y+h, x:x+W]
                            return face_cropped
                    
                    cap = cv2.VideoCapture(0)
                    img_id = 0
                    while True:
                        ret, my_frame = cap.read()
                        if face_cropped(my_frame) is not None:
                            img_id += 1
                            face = cv2.resize(face_cropped(my_frame),(450,450))
                            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                            file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
                            cv2.imwrite(file_name_path,face)
                            cv2.putText(face, str(img_id),(50,50), cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                            cv2.imshow("cropped face", face)

                        if cv2.waitKey(1)==13 or int(img_id) == 100:
                            break
                    
                    cap.release()
                    cv2.destroyAllWindows()
                except Exception as es:
                    messagebox.showinfo("Result", "Generation of dataset completed!")





if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()