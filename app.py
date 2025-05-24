from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# Debug info
print("📂 Current working directory:", os.getcwd())

# Model path and existence check
model_path = '1.h5'
print(f"🔍 Checking if model file exists at: {model_path} =>", os.path.exists(model_path))

# Load the model once
model = None
try:
    print("📦 Attempting to load model...")
    model = tf.keras.models.load_model(model_path)
    print("✅ Model loaded successfully.")
    model.summary()
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    model = None

# Sample class names
class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# Grad-CAM utility functions
def grad_cam(input_model, image, layer_name="block_16_project_BN"):
    grad_model = tf.keras.models.Model(
        inputs=[input_model.input],
        outputs=[input_model.get_layer(layer_name).output, input_model.output]
    )
    with tf.GradientTape() as tape:
        tape.watch(image)
        conv_output, predictions = grad_model(image)
        predicted_class = tf.argmax(predictions[0])
        grads = tape.gradient(predictions[0][predicted_class], conv_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_output = conv_output[0]
    heatmap = tf.reduce_sum(conv_output * pooled_grads, axis=-1)
    heatmap = tf.maximum(heatmap, 0)
    heatmap /= tf.reduce_max(heatmap)
    return heatmap.numpy()

def overlay_heatmap(image_np, heatmap, alpha=0.4):
    heatmap_resized = cv2.resize(heatmap, (image_np.shape[1], image_np.shape[0]))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    image_inverted = cv2.bitwise_not(image_np)
    overlayed = cv2.addWeighted(image_inverted, 1 - alpha, heatmap_colored, alpha, 0)
    return overlayed

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model failed to load on server startup. Please check server logs.'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected image'}), 400

    try:
        image = Image.open(file).convert('RGB')
        image = image.resize((224, 224))
        image_array = np.array(image)
        image_input = np.expand_dims(image_array / 255.0, axis=0)

        predictions = model.predict(image_input)
        print("Prediction raw output:", predictions)

        if len(class_names) != predictions.shape[1]:
            return jsonify({
                'error': f'Class mismatch: model returned {predictions.shape[1]} classes, but {len(class_names)} class names are defined.'
            }), 500

        predicted_index = np.argmax(predictions)
        predicted_label = class_names[predicted_index]

        # Convert raw predictions to list of floats
        probabilities = predictions[0].tolist()

        # Generate Grad-CAM
        heatmap = grad_cam(model, tf.convert_to_tensor(image_input, dtype=tf.float32))
        overlayed_image = overlay_heatmap(image_array, heatmap)

        # Ensure static folder exists
        os.makedirs('static', exist_ok=True)
        heatmap_path = 'static/heatmap.jpg'
        cv2.imwrite(heatmap_path, overlayed_image)

        return jsonify({
            'prediction': predicted_label,
            'probabilities': probabilities,
            'heatmap_url': heatmap_path
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Debug: print all registered routes
print("🔗 Registered routes:")
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
