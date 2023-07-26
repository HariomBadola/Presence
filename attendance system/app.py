from flask import Flask, render_template, request
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('web.html')


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    image_data = request.form['image']

    # Create a folder if it doesn't exist
    if not os.path.exists("face_img"):
        os.makedirs("face_img")
    img_path = f"face_img/{student_id}.jpg"
    
    # Save the image using base64 decoding
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    print(f"Image saved as {img_path}")

    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)
