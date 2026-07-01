from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np


#=================attendence marking module===========
def mark_attendence(self,r,d,y):
    with open("attSheet.csv","r+", newline="\n") as f:
        myDataList = f.readlines()
        name_list =[]
        for line in myDataList:
            entry = line.split((","))
            name_list.append(entry[0])

        if((r not in name_list) and (r not in name_list) and (y not in name_list)):
            now = datetime.now()
            d1 = now.strftime("%d/%m/%Y")
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{r},{d},{y},Present")



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
            if img is None or img.size == 0:
                print("Error: Input image to draw_boundary is invalid")
                return []

            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            print(f"Detected {len(features)} faces")

            coord = []
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                face_region = gray_image[y:y + h, x:x + w]
                if face_region.size == 0:
                    print("Error: Face region is empty")
                    continue

                try:
                    id, predict = clf.predict(face_region)
                    confidence = int((100 * (1 - predict / 300)))
                except Exception as e:
                    print(f"Error in clf.predict: {str(e)}")
                    continue

                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="v26qtE%$11",
                    database="facerecognition_att"
                )
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT roll_no FROM student WHERE roll_no=%s", (id,))
                roll_no = my_cursor.fetchone()
                roll_no = str(roll_no[0]) if roll_no else "Unknown"

                my_cursor.execute("SELECT Dep FROM student WHERE roll_no=%s", (id,))
                dept = my_cursor.fetchone()
                dept = str(dept[0]) if dept else "Unknown"

                my_cursor.execute("SELECT year FROM student WHERE roll_no=%s", (id,))
                year = my_cursor.fetchone()
                year = str(year[0]) if year else "Unknown"

                conn.close()

                if confidence > 80:
                    cv2.putText(img, f"Roll:{roll_no}", (x, y - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Department:{dept}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(img, f"Year:{year}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
                    self.mark_attendence(roll_no,dept,year)

                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 1)

                coord = [x, y, w, h]

            return coord

        def recognizzer(img, clf, faceCascade):
            if img is None or img.size == 0:
                print("Error: Input image to recognizzer is invalid")
                return img

            coord = draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "FACE", clf)
            return img

        # Load Haar Cascade classifier
        faceCascade22 = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if faceCascade22.empty():
            messagebox.showerror("Error", "Failed to load Haar Cascade classifier")
            return

        # Load face recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        try:
            clf.read("classifier/classifier.xml")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classifier: {str(e)}")
            return

        # Try opening the camera with different indices
        for index in [0, 1]:
            video_cap = cv2.VideoCapture(index)
            if video_cap.isOpened():
                print(f"Camera opened successfully with index {index}")
                break
        else:
            messagebox.showerror("Error", "Could not open any webcam. Please check camera connection or try a different index.")
            return

        # Explicitly create the OpenCV window
        window_name = "Face Detection"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 800, 600)

        while True:
            ret, img = video_cap.read()
            if not ret or img is None or img.size == 0:
                messagebox.showerror("Error", "Failed to capture frame from camera. Please check camera connection.")
                video_cap.release()
                cv2.destroyAllWindows()
                break

            print(f"Raw frame captured: {img.shape}")

            # Resize the frame
            img = cv2.resize(img, (800, 600))
            print(f"Frame after resize: {img.shape}")

            # Process the frame for face detection and recognition
            img_processed = recognizzer(img, clf, faceCascade22)
            if img_processed is None or img_processed.size == 0:
                print("Error: Processed frame is invalid, displaying raw frame instead")
                img_processed = img  # Fallback to raw frame

            print(f"Frame after processing: {img_processed.shape}")

            # Display the frame
            cv2.imshow(window_name, img_processed)

            # Add a delay to allow the window to update
            key = cv2.waitKey(10)
            if key == 13:  # Enter key to break
                break

        # Clean up
        video_cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed")


if __name__ == "__main__":
    root = Tk()
    obj = Face_Detector(root)
    root.mainloop()