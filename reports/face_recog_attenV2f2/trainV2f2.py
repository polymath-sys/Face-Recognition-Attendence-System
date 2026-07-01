from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np


class Train:
    """
    Face recognition training module.
    Trains the face recognition model using collected face images.
    """
    
    def __init__(self, root: Tk):
        """
        Initialize the training window.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.geometry("800x500+300+150")  # Smaller window size
        self.root.title("Train Face Recognition Model")
        self.root.configure(bg="#f0f0f0")

        self._setup_ui()

    def _setup_ui(self):
        """Setup the user interface components."""
        # Title Label
        title_lbl = Label(
            self.root,
            text="Train Face Recognition Model",
            font=("Helvetica", 20, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        title_lbl.pack(pady=20)

        # Info Frame
        info_frame = Frame(self.root, bg="#f0f0f0")
        info_frame.pack(pady=20)

        # Information Label
        info_text = (
            "This will train the face recognition model using all\n"
            "the face images stored in the 'data' directory.\n\n"
            "Make sure you have collected sufficient face samples\n"
            "before training the model."
        )
        
        Label(
            info_frame,
            text=info_text,
            font=("Helvetica", 12),
            bg="#f0f0f0",
            justify=LEFT
        ).pack()

        # Train Button
        train_btn = Button(
            self.root,
            text="TRAIN MODEL",
            command=self.train_classifier,
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            bd=0,
            activebackground="#2980b9"
        )
        train_btn.pack(pady=30)

        # Status Label
        self.status_label = Label(
            self.root,
            text="Ready to train...",
            font=("Helvetica", 12),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.status_label.pack()

    def train_classifier(self):
        """
        Train the face recognition classifier using collected face images.
        """
        self.status_label.config(text="Training in progress...", fg="#e67e22")
        self.root.update()  # Force UI update

        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                raise FileNotFoundError(f"Directory '{data_dir}' not found")

            # Get list of image paths
            image_paths = [
                os.path.join(data_dir, f) 
                for f in os.listdir(data_dir) 
                if f.endswith('.jpg')
            ]

            if not image_paths:
                raise ValueError("No face images found in 'data' directory")

            faces = []
            ids = []

            # Process each image
            for path in image_paths:
                try:
                    # Read and convert to grayscale
                    img = Image.open(path).convert('L')
                    img_np = np.array(img, 'uint8')

                    # Extract ID from filename (format: user.ID.number.jpg)
                    file_name = os.path.split(path)[1]
                    user_id = int(file_name.split('.')[1])

                    faces.append(img_np)
                    ids.append(user_id)

                    # Show training progress
                    cv2.imshow("Training", img_np)
                    if cv2.waitKey(1) == 27:  # ESC to exit
                        break

                except Exception as e:
                    print(f"Skipping {path}: {str(e)}")
                    continue

            cv2.destroyAllWindows()

            if not faces:
                raise ValueError("No valid face images found for training")

            # Convert IDs to numpy array
            ids = np.array(ids)

            # Initialize and train the recognizer
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
            except AttributeError:
                raise ImportError(
                    "OpenCV face module not found. Install opencv-contrib-python:\n"
                    "pip install opencv-contrib-python"
                )

            recognizer.train(faces, ids)

            # Create classifier directory if not exists
            os.makedirs("classifier", exist_ok=True)

            # Save the trained model
            model_path = "classifier/classifier.xml"
            recognizer.save(model_path)

            self.status_label.config(
                text=f"Training completed successfully!\nModel saved to {model_path}",
                fg="#27ae60"
            )
            messagebox.showinfo(
                "Success",
                "Training completed successfully!",
                parent=self.root
            )

        except Exception as e:
            self.status_label.config(text="Training failed", fg="#e74c3c")
            messagebox.showerror(
                "Error",
                f"Training failed:\n{str(e)}",
                parent=self.root
            )
            print(f"Training error: {str(e)}")


if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()