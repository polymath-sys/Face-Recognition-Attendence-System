from tkinter import *
from tkinter import messagebox
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

        self.detect_face_btn = Button(self.root, text="Detect Face", command=self.face_detector,
                                     cursor="hand2", font=("arial", 18, "bold"), bg="green", fg="white")
        self.detect_face_btn.place(x=520, y=300, width=200, height=60)

    def face_detector(self):
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])
                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(host="localhost", username="root", password="v26qtE%$11",
                                               database="facerecognition_att")
                my_cursor = conn.cursor()

                my_cursor.execute("select roll_no from student where roll_no=%s", (id,))
                r = my_cursor.fetchone()
                r = str(r[0]) if r else "Unknown"

                my_cursor.execute("select Dep from student where roll_no=%s", (id,))
                d = my_cursor.fetchone()
                d = str(d[0]) if d else "Unknown"

                my_cursor.execute("select year from student where roll_no=%s", (id,))
                y = my_cursor.fetchone()
                y = str(y[0]) if y else "Unknown"

                if confidence > 77:
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Year: {y}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord = [x, y, w, h]

            return coord

        def recognizzer(img, clf, faceCascade):
            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "FACE", clf)
            return img

        # Load Haar cascade
        faceCascade22 = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        if faceCascade22.empty():
            messagebox.showerror("Error", "Failed to load Haar Cascade XML file.")
            return

        # Load trained recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        if not os.path.exists("classifier/classifier.xml"):
            messagebox.showerror("Error", "Trained classifier file not found.")
            return

        clf.read("classifier/classifier.xml")

        # Start video stream
        video_cap = cv2.VideoCapture(0)
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        cv2.namedWindow("Hello! alligator", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Hello! alligator", 800, 600)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            img = recognizzer(img, clf, faceCascade22)
            cv2.imshow("Hello! alligator", img)

            if cv2.waitKey(1) == 13:  # Enter key
                break

        video_cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    obj = Face_Detector(root)
    root.mainloop()
