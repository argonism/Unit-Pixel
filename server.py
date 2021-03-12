from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import os
import string
from PIL import Image
from face2pixel import Face2Pixel
from utils import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = "static"
RESULT_DIR = "tmp"
SOURCE_DIR = "templates"
app = Flask(__name__, static_folder=STATIC_DIR)

def source_dir(file_name):
    return f"{file_name}"

def load_model():
    global model
    print(" * Loading pre-trained model ...")
    model = Face2Pixel()
    print(' * Loading end')

@app.route('/')
def index():
    return render_template(source_dir('index.html'))

@app.route('/pixelation', methods=['POST'])
def pixelation():
    if request.files['image']:
        in_img = request.files['image']
        image_pil = image_to_pil(in_img)
         
        if image_pil.width > 1000 or image_pil.height > 1000:
            image_pil = resize_length(image_pil, 1000)
            print(f"resized: {image_pil.width}, {image_pil.height}")

        image_rgb = image_pil.convert("RGB")
        result_filename = model.convert_image(image_rgb)
        return redirect(url_for('result', filename=result_filename))

    return redirect(url_for('index'))

@app.route('/result/<filename>')
def result(filename):
    result_path = f"/{STATIC_DIR}/{RESULT_DIR}/{filename}.png"
    return render_template(source_dir('result.html'), title='生成結果', result_path=result_path)

if __name__ == '__main__':
    load_model()
    app.run(host='localhost', port=3000, debug=True)