from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os  # Added to help with file checks

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Debug info: print current working directory
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

# Sample class names - make sure these match your model output
class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

@app.route('/', methods=['GET'])
def home():
    return 'Flask API is working!'

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
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)
        print("Prediction raw output:", predictions)

        if len(class_names) != predictions.shape[1]:
            return jsonify({
                'error': f'Class mismatch: model returned {predictions.shape[1]} classes, but {len(class_names)} class names are defined.'
            }), 500

        predicted_index = np.argmax(predictions)
        predicted_label = class_names[predicted_index]

        return jsonify({'prediction': predicted_label})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Print all routes for debugging
print("🔗 Registered routes:")
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
