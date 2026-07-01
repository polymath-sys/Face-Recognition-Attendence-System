from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import numpy as np

class Face_Detector:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Face Detector")

        title_lbl = Label(self.root, text="Face Detector", font=("", 30, "bold"), fg="brown")
        title_lbl.place(x=0, y=0, width=1750, height=50)

        self.detect_face_btn = Button(self.root, text="Detect Face",command=self.face_detector,
                                     cursor="hand2", font=("arial", 18, "bold"), bg="green", fg="white")
        self.detect_face_btn.place(x=520, y=300, width=200, height=60)


        #===============face detector===========

    def face_detector(self):
            def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, cls):
                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

                coord = []

                for(x,y,w,h) in features:
                    cv2.rectangle(img,(x,y), (x+w, y+h), (0,255,0),3)
                    id, predict =clf.predict(gray_image[y:y+h, x:x+w])
                    confidence = int((100*(1-predict/300)))

                    #we are taking data here from database
                    conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                                  database="facerecognition_att")
                    my_cursor = conn.cursor()

                    my_cursor.execute("select roll_no from student where roll_no="+str(id))
                    r = my_cursor.fetchone()
                    r = "+".join(r)

                    my_cursor.execute("select Dep from student where roll_no="+str(id))
                    d = my_cursor.fetchone()
                    d = "+".join(d)

                    my_cursor.execute("select year from student where roll_no="+str(id))
                    y = my_cursor.fetchone()
                    y = "+".join(y)

                    if confidence > 77:
                        cv2.putText(img, f"Roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                        cv2.putText(img, f"Department:{d}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                        cv2.putText(img, f"Year:{y}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                    else:
                        cv2.rectangle(img(x,y), (x+w, y+h), (0,0,255),3)
                        cv2.putText(img, "Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)

                        coord=[x,y,w,h]

                    return coord
                
                def recognizzer(img,clf,faceCascade):
                    coord = draw_boundary(img,faceCascade,1.1,10,(255,255,255),"FACE",clf)
                    return img
                
                faceCascade22 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.read("classifier/classifier.xml")

                video_cap = cv2.VideoCapture(0)

                while True:
                    ret, img = video_cap.read()
                    img = recognizzer(img, clf,faceCascade22)
                    cv2.imshow("Hello! alligator",img)

                    if cv2.waitKey(1) == 13:
                        break
                    video_cap.release()
                    cv2.destroyAllWindows()
        




if __name__ == "__main__":
    root = Tk()
    obj = Face_Detector(root)
    root.mainloop()