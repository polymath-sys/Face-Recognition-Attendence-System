from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1750x858+0+0")
        self.root.title("Train Face")

        title_lbl = Label(self.root, text="Train Data-Set",font=("", 30, "bold"), fg="brown")
        title_lbl.place(x=0, y=0, width=1750, height=50)

        self.train_data_btn = Button(self.root, text="TRAIN DATA", command=self.train_classifier, cursor="hand2", font=("", 13, "bold"), bg="grey", fg="black")

        self.train_data_btn.place(x=520, y=300, width=200, height=60)

    def train_classifier(self):
        data_dir = ("data")
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L') #gray scale image
            imageNp =np.array(img, 'uint8') #to convert into grid system
            id = int(os.path.split(image)[1].split('.')[1])

            # C:\Users\788ad\OneDrive\Desktop\face_recognition_system\data\user.1300311.1.jpg
            # (---------index - 0-----------------------------------------)(---index-1------)

            faces.append(imageNp)
            ids.append(id)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1) == 13

        ids = np.array(ids)

        #===============Train the classifier and save===============
        if len(faces) == 0 or len(ids) == 0:
            messagebox.showerror("Error", "No data found to train.")
            return

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        os.makedirs("classifier", exist_ok=True)
        clf.write("classifier/classifier.xml")

        # clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training of dataset completed!!")



if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()