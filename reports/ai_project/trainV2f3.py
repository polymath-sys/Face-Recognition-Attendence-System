from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        """Initialize the Train Face window."""
        self.root = root
        self.root.geometry("1280x720+0+0")  # Adjusted for smaller screens
        self.root.title("Train Face")
        self.root.configure(bg="#f0f0f0")  # Light background

        # Title label
        title_lbl = Label(self.root, text="Train Data-Set", font=("Helvetica", 24, "bold"), 
                         fg="#2c3e50", bg="#f0f0f0")
        title_lbl.place(relx=0.5, rely=0.1, anchor="center")

        # Train Data button
        self.train_data_btn = Button(self.root, text="Train Data", command=self.train_classifier,
                                    cursor="hand2", font=("Helvetica", 14, "bold"), 
                                    bg="#7f8c8d", fg="white", width=15, height=2)
        self.train_data_btn.place(relx=0.5, rely=0.5, anchor="center")

    def train_classifier(self):
        """Train the face recognition classifier using images in 'data' directory."""
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", f"'{data_dir}' folder not found.")
            return

        # Collect image paths
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
        faces = []
        ids = []

        for image in path:
            try:
                # Convert image to grayscale
                img = Image.open(image).convert('L')
                imageNp = np.array(img, 'uint8')
                # Extract ID from filename (format: user.ID.x.jpg)
                id = int(os.path.split(image)[1].split('.')[1])

                faces.append(imageNp)
                ids.append(id)

                # Display image during training
                cv2.imshow("Training", imageNp)
                cv2.waitKey(1)

            except Exception as e:
                print(f"Error processing image {image}: {e}")

        cv2.destroyAllWindows()

        if len(faces) == 0 or len(ids) == 0:
            messagebox.showerror("Error", "No valid data found for training.")
            return

        try:
            # Create and train the classifier
            clf = cv2.face.LBPHFaceRecognizer_create()
            ids = np.array(ids)
            clf.train(faces, ids)

            # Save classifier
            os.makedirs("classifier", exist_ok=True)
            clf.write("classifier/classifier.xml")
            messagebox.showinfo("Result", "Training completed successfully!")

        except AttributeError:
            messagebox.showerror("OpenCV Error", "cv2.face module not found. Install opencv-contrib-python.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()