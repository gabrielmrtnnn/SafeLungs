from flask import Flask, request, render_template, jsonify
from ultralytics import YOLO
from PIL import Image
import numpy as np
import io

# Inisialisasi Flask
app = Flask(__name__)

# Load YOLOv8 Classification model
MODEL_PATH = "best.pt"
model = YOLO(MODEL_PATH)

# Halaman utama
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# API untuk prediksi
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        # Baca file gambar
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # Prediksi dengan YOLOv8
        results = model(img)

        # Ambil probabilitas dan kelas prediksi
        probs = results[0].probs.data.cpu().numpy()
        pred_idx = np.argmax(probs)
        pred_class = model.names[pred_idx]
        confidence = probs[pred_idx]

        return jsonify({
            "prediction": pred_class,
            "confidence": float(confidence)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Untuk local debug
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
