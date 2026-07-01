from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk
import mysql.connector
from time import strftime
from datetime import datetime
import cv2
import os
import numpy as np

class Face_Detector:
    def __init__(self, root):
        """Initialize the Face Detector window."""
        self.root = root
        self.root.geometry("1280x720+0+0")  # Adjusted for smaller screens
        self.root.title("Face Detector")
        self.root.configure(bg="#f0f0f0")  # Light background

        # Title label
        title_lbl = Label(self.root, text="Face Detector", font=("Helvetica", 24, "bold"), 
                         fg="#2c3e50", bg="#f0f0f0")
        title_lbl.place(relx=0.5, rely=0.1, anchor="center")

        # Detect Face button
        self.detect_face_btn = Button(self.root, text="Detect Face", command=self.face_detector,
                                     cursor="hand2", font=("Helvetica", 14, "bold"), 
                                     bg="#27ae60", fg="white", width=15, height=2)
        self.detect_face_btn.place(relx=0.5, rely=0.5, anchor="center")

    def mark_attendence(self, roll_no, dept, year):
        """Mark attendance in CSV file if not already recorded."""
        with open("attSheet.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = [line.split(",")[0] for line in myDataList]

            if roll_no not in name_list and dept not in name_list and year not in name_list:
                now = datetime.now()
                date = now.strftime("%d/%m/%Y")
                time = now.strftime("%H:%M:%S")
                f.writelines(f"\n{roll_no},{dept},{year},{time},{date},Present")

    def face_detector(self):
        """Detect and recognize faces using webcam feed."""
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            """Draw rectangles around detected faces and label with student info."""
            if img is None or img.size == 0:
                print("Error: Invalid input image")
                return []

            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            print(f"Detected {len(features)} faces")

            coord = []
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
                face_region = gray_image[y:y + h, x:x + w]
                if face_region.size == 0:
                    print("Error: Empty face region")
                    continue

                try:
                    id, predict = clf.predict(face_region)
                    confidence = int((100 * (1 - predict / 300)))
                except Exception as e:
                    print(f"Error in clf.predict: {str(e)}")
                    continue

                # Connect to database
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
                    self.mark_attendence(roll_no, dept, year)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 1)

                coord.append([x, y, w, h])

            return coord

        def recognizzer(img, clf, face_cascade):
            """Process image for face detection and recognition."""
            if img is None or img.size == 0:
                print("Error: Invalid input image")
                return img

            coord = draw_boundary(img, face_cascade, 1.1, 10, (255, 255, 255), "FACE", clf)
            return img

        # Load Haar Cascade classifier
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if face_cascade.empty():
            messagebox.showerror("Error", "Failed to load Haar Cascade classifier")
            return

        # Load face recognizer
        clf = cv2.face.LBPHFaceRecognizer_create()
        try:
            clf.read("classifier/classifier.xml")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load classifier: {str(e)}")
            return

        # Try opening the camera
        for index in [0, 1]:
            video_cap = cv2.VideoCapture(index)
            if video_cap.isOpened():
                print(f"Camera opened successfully with index {index}")
                break
        else:
            messagebox.showerror("Error", "Could not open webcam. Check camera connection.")
            return

        # Create OpenCV window
        window_name = "Face Detection"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)  # Adjusted for smaller screens

        while True:
            ret, img = video_cap.read()
            if not ret or img is None or img.size == 0:
                messagebox.showerror("Error", "Failed to capture frame from camera.")
                video_cap.release()
                cv2.destroyAllWindows()
                break

            print(f"Raw frame captured: {img.shape}")

            # Resize frame
            img = cv2.resize(img, (640, 480))
            print(f"Frame after resize: {img.shape}")

            # Process frame
            img_processed = recognizzer(img, clf, face_cascade)
            if img_processed is None or img_processed.size == 0:
                print("Error: Processed frame is invalid, displaying raw frame")
                img_processed = img

            print(f"Frame after processing: {img_processed.shape}")

            # Display frame
            cv2.imshow(window_name, img_processed)

            # Exit on Enter key
            key = cv2.waitKey(10)
            if key == 13:
                break

        # Cleanup
        video_cap.release()
        cv2.destroyAllWindows()
        print("Camera released and windows closed")

if __name__ == "__main__":
    root = Tk()
    obj = Face_Detector(root)
    root.mainloop()