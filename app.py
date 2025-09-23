from flask import Flask, request, render_template
import os
os.environ["ULTRALYTICS_IGNORE_GIT"] = "1"
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import os

# Inisialisasi Flask
app = Flask(__name__)

# Load YOLOv8 Classification model
MODEL_PATH = "best.pt"

import torch

# Override default load agar weights_only=False
_orig_load = torch.load
def load_weights_only_false(*args, **kwargs):
    kwargs["weights_only"] = False
    return _orig_load(*args, **kwargs)
torch.load = load_weights_only_false


model = YOLO(MODEL_PATH)

# Set the folder to store uploaded images temporarily
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Halaman utama
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# API untuk prediksi
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return render_template("index.html", error="No file uploaded")

    file = request.files["file"]

    try:
        # Save the uploaded file temporarily
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(img_path)

        # Baca file gambar
        img = Image.open(img_path).convert("RGB")

        # Prediksi dengan YOLOv8
        results = model(img)

        # Ambil probabilitas dan kelas prediksi
        probs = results[0].probs.data.cpu().numpy()
        pred_idx = np.argmax(probs)
        pred_class = model.names[pred_idx]
        confidence = probs[pred_idx]

        # Render the HTML template with the prediction results
        return render_template(
            "index.html",
            prediction=pred_class,
            confidence=f"{confidence * 100:.2f}",
            img_path=img_path  # Pass the path of the saved image to the template
        )

    except Exception as e:
        return render_template("index.html", error=f"Prediction failed: {e}")

# Untuk local debug
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)