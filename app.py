from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import cv2
import uuid

app = Flask(__name__)
CORS(app)

model_path = '1.h5'
model = None
try:
    model = tf.keras.models.load_model(model_path)
    print("✅ Model loaded.")
except Exception as e:
    print("❌ Model loading failed:", e)

class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

def grad_cam(model, image, layer_name="block_16_project_BN"):
    grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(image)
        class_idx = tf.argmax(predictions[0])
        output = predictions[:, class_idx]
        grads = tape.gradient(output, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        return heatmap.numpy()

def overlay_heatmap(orig_img, heatmap, alpha=0.4):
    heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
    return blended

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded.'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    image = Image.open(file).convert('RGB')
    image = image.resize((224, 224))
    np_img = np.array(image)
    input_img = np.expand_dims(np_img / 255.0, axis=0)

    predictions = model.predict(input_img)
    prediction_idx = np.argmax(predictions[0])
    prediction_label = class_names[prediction_idx]
    probabilities = predictions[0].tolist()

    # Grad-CAM and heatmap overlay
    heatmap = grad_cam(model, input_img)
    overlay = overlay_heatmap(np_img, heatmap)

    heatmap_filename = f"{uuid.uuid4().hex}.jpg"
    heatmap_path = os.path.join("static", heatmap_filename)
    if not os.path.exists("static"):
        os.makedirs("static")
    cv2.imwrite(heatmap_path, overlay)

    return jsonify({
        'prediction': prediction_label,
        'probabilities': probabilities,
        'heatmap_url': f"static/{heatmap_filename}"
    })

@app.route('/static/<filename>')
def serve_heatmap(filename):
    return send_from_directory('static', filename)
