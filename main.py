from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from studentV2f import Student  # Make sure 'student.py' is in the same folder 
import os
from trainV2f import Train
from face_detectorV2f import Face_Detector
from attendenceV2f import Attendance



class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Face Recognition System")

        # BG Image
        img3 = Image.open(r"assets\bg.png")
        img3 = img3.resize((720, 200), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.bg_image)
        bg_img.place(x=520, y=550, width=720, height=200)

        # Title Label
        title_lbl = Label(self.root, text="Face Recognition Attendance System \n Made By-", font=("", 30, "bold"), fg="blue")
        title_lbl.place(x=0, y=150, width=1750, height=100)

        # Names Label
        names_lbl = Label(self.root, text="Aditya Pandey", font=("", 20, "bold"), fg="blue")
        names_lbl.place(x=0, y=250, width=1750, height=100)

        # Buttons
        self.student_btn = Button(self.root, text="Student", command=self.student_details, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")
        self.student_btn.place(x=520, y=500, width=100, height=40)

        self.detect_face_btn = Button(self.root, text="Detect Face",command=self.detect_face, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")
        self.detect_face_btn.place(x=650, y=500, width=100, height=40)

        self.attendance_btn = Button(self.root, text="Attendance",command=self.attendance_data, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")
        self.attendance_btn.place(x=780, y=500, width=100, height=40)

        self.train_face_btn = Button(self.root, text="Train Face",command=self.train_data, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")
        self.train_face_btn.place(x=910, y=500, width=100, height=40)

        self.train_face_btn = Button(self.root, text="Photos", command=self.open_img, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")
        self.train_face_btn.place(x=1020, y=500, width=100, height=40)


    def open_img(self):
        os.startfile("data")

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

     
    def detect_face(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Detector(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

# Run the App
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()










'''from tkinter import*
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from tkinter import Toplevel

class Face_Recognition_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Face Recognititon System")

#BG Image
        img3= Image.open(r"assets\bg.png")
        img3 = img3.resize((720, 200), Image.Resampling.LANCZOS) #(1750, 858)
        self.bg_image= ImageTk.PhotoImage(img3)
            
        bg_img = Label(self.root, image = self.bg_image)
        bg_img.place(x=520, y=550, width=720, height=200) #width=root.winfo_screenwidth(), height=root.winfo_screenheight()

#Title Label
        #bg_img, text="Face Recognition Attendence Shyshtem", font=("",30,"bold"), fg="blue"
        title_lbl = Label(text="Face Recognition Attendence Shyshtem \n Made By-", font=("",30,"bold"), fg="blue")
        title_lbl.place(x=0, y=150, width=1750, height=100)
#names label
        names_lbl = Label(text="Aditya Pandey(102303968)\n Yash Vardhan Singh(102303725) \n Mehul Kujur(102303712)", font=("",20,"bold"), fg="blue")
        names_lbl.place(x=0, y=250, width=1750, height=100)

#Student Button
        self.student_btn = Button(self.root, text="Student",command=self.student_details, cursor="hand2", font=("",13,"bold"), bg="grey", fg="black")
        self.student_btn.place(x=520, y=500, width=100, height=40)
        self.student_btn.pack()


#Detect face Button
        self.detect_btn = Button(self.root, text="Detect Face", cursor="hand2", font=("",13,"bold"), bg="grey", fg="black")
        self.detect_btn.place(x=650, y=500, width=100, height=40)

#Attendance Button
        self.attendence_btn = Button(self.root, text="Attendance", cursor="hand2", font=("",13,"bold"), bg="grey", fg="black")
        self.attendence_btn.place(x=780, y=500, width=100, height=40)

#Train Face Button
        self.train_face_btn = Button(self.root, text="Train Face", cursor="hand2", font=("",13,"bold"), bg="grey", fg="black")
        self.train_face_btn.place(x=910, y=500, width=100, height=40)

#=====FUNCTION BUTTONS===================
    

        def student_details(self):
                self.new_window = Toplevel(self.root)
                self.app = Student(self.new_window)
if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()'''