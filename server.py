from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import os
import string
from PIL import Image
from face2pixel import Face2Pixel

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = "static"
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

@app.route('/result', methods=['POST'])
def result():
    if request.files['image']:
        image_pil = Image.open(request.files['image'])
        image_rgb = image_pil.convert("RGB")
        result_path = model.convert_image(image_rgb)
        return render_template(source_dir('result.html'), title='生成結果', result_path=result_path)

if __name__ == '__main__':
    load_model()
    app.debug = True
    app.run(host='localhost', port=3000)