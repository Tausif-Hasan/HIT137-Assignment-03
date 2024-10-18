import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

# ModelHandler class handles the loading and prediction of the AI model
class ModelHandler:
    def __init__(self):
        self.model = MobileNetV2(weights='imagenet')  # Load the MobileNetV2 pre-trained model
    
    def preprocess_image(self, img):
        img = img.resize((224, 224))  # Resize image to 224x224 for MobileNetV2
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return preprocess_input(img_array)

    def predict(self, img):
        processed_img = self.preprocess_image(img)
        predictions = self.model.predict(processed_img)
        decoded_predictions = decode_predictions(predictions, top=3)[0]
        return decoded_predictions

class App(tk.Frame, ModelHandler):  
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)  # Initialize Tkinter Frame
        ModelHandler.__init__(self)  # Initialize ModelHandler
        self.master = master
        self.master.title("Image Classifier")
        self.pack()

        # Tkinter widgets
        self.label = Label(self, text="Choose an Image to Classify", font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.image_label = Label(self)  # Label to display the selected image
        self.image_label.pack()

        self.button = Button(self, text="Select Image", command=self.load_image)
        self.button.pack(pady=10)

        self.classify_button = Button(self, text="Classify Image", command=self.classify_image)
        self.classify_button.pack(pady=10)

        self.result_label = Label(self, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        self.image = None  # Variable to store the image

    def load_image(self):
        image_path = filedialog.askopenfilename()  # Open file dialog to select an image
        if image_path:
            self.image = Image.open(image_path)  # Open the image using Pillow
            self.show_image(self.image)

    def show_image(self, img):
        img = img.resize((150, 150))  # Resize image for display
        img_tk = ImageTk.PhotoImage(img)  # Convert image to format suitable for Tkinter
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk  # Keep a reference to avoid garbage collection

    def classify_image(self):
        if self.image:
            predictions = self.predict(self.image)  # Call ModelHandler's predict method
            self.show_results(predictions)

    def show_results(self, predictions):
        result_text = ""
        for pred in predictions:
            result_text += f"{pred[1]}: {pred[2]*100:.2f}%\n"
        self.result_label.config(text=result_text)

# Function to run the GUI
def run_gui():
    root = tk.Tk()  # Create root window
    app = App(master=root)
    app.mainloop()  # Start Tkinter event loop

if __name__ == "__main__":
    run_gui()
