# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import uuid

# app = Flask(__name__)
# CORS(app)

# model_path = '1.h5'
# model = None
# try:
#     model = tf.keras.models.load_model(model_path)
#     print("✅ Model loaded.")
# except Exception as e:
#     print("❌ Model loading failed:", e)

# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# def grad_cam(model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
#     with tf.GradientTape() as tape:
#         conv_outputs, predictions = grad_model(image)
#         class_idx = tf.argmax(predictions[0])
#         output = predictions[:, class_idx]
#         grads = tape.gradient(output, conv_outputs)
#         pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#         conv_outputs = conv_outputs[0]
#         heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
#         heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#         return heatmap.numpy()

# def overlay_heatmap(orig_img, heatmap, alpha=0.4):
#     heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
#     return blended

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     file = request.files['image']
#     image = Image.open(file).convert('RGB')
#     image = image.resize((224, 224))
#     np_img = np.array(image)
#     input_img = np.expand_dims(np_img / 255.0, axis=0)

#     predictions = model.predict(input_img)
#     prediction_idx = np.argmax(predictions[0])
#     prediction_label = class_names[prediction_idx]
#     probabilities = predictions[0].tolist()

#     # Grad-CAM and heatmap overlay
#     heatmap = grad_cam(model, input_img)
#     overlay = overlay_heatmap(np_img, heatmap)

#     heatmap_filename = f"{uuid.uuid4().hex}.jpg"
#     heatmap_path = os.path.join("static", heatmap_filename)
#     if not os.path.exists("static"):
#         os.makedirs("static")
#     cv2.imwrite(heatmap_path, overlay)

#     return jsonify({
#         'prediction': prediction_label,
#         'probabilities': probabilities,
#         'heatmap_url': f"static/{heatmap_filename}"
#     })

# @app.route('/static/<filename>')
# def serve_heatmap(filename):
#     return send_from_directory('static', filename)




# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import matplotlib.pyplot as plt
# import requests
# import uuid

# app = Flask(__name__)
# CORS(app)

# # Debug info
# print("📂 Current working directory:", os.getcwd())

# # Model path and existence check
# model_path = '1.h5'
# print(f"🔍 Checking if model file exists at: {model_path} =>", os.path.exists(model_path))

# # Load the model once
# model = None
# try:
#     print("📦 Attempting to load model...")
#     model = tf.keras.models.load_model(model_path)
#     print("✅ Model loaded successfully.")
#     model.summary()
# except Exception as e:
#     print(f"❌ Error loading model: {str(e)}")
#     model = None

# # Sample class names
# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']



# #remove background function using rembg API

# def remove_background(image_path):
#     url = "https://api.rembg.com/rmbg"
#     headers = {
#         "x-api-key": "70d943a9-621f-4107-a1e1-6d3f48901083"
#     }

#     with open(image_path, "rb") as img_file:
#         files = {"image": img_file}
#         response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         unique_filename = f"{uuid.uuid4().hex}_nobg.png"
#         output_path = os.path.join("static", unique_filename)
#         with open(output_path, "wb") as out_file:
#             out_file.write(response.content)
#         return output_path
#     else:
#         print("❌ Background removal failed:", response.status_code, response.text)
#         return None


# # Grad-CAM utility functions
# def grad_cam(input_model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model(
#         inputs=[input_model.input],
#         outputs=[input_model.get_layer(layer_name).output, input_model.output]
#     )
#     with tf.GradientTape() as tape:
#         tape.watch(image)
#         conv_output, predictions = grad_model(image)
#         predicted_class = tf.argmax(predictions[0])
#         grads = tape.gradient(predictions[0][predicted_class], conv_output)
#     pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#     conv_output = conv_output[0]
#     heatmap = tf.reduce_sum(conv_output * pooled_grads, axis=-1)
#     heatmap = tf.maximum(heatmap, 0)
#     heatmap /= tf.reduce_max(heatmap)
#     return heatmap.numpy()

# def overlay_heatmap(image_np, heatmap, alpha=0.4):
#     heatmap_resized = cv2.resize(heatmap, (image_np.shape[1], image_np.shape[0]))
#     heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
#     image_inverted = cv2.bitwise_not(image_np)
#     overlayed = cv2.addWeighted(image_inverted, 1 - alpha, heatmap_colored, alpha, 0)
#     return overlayed
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model failed to load on server startup. Please check server logs.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400

#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({'error': 'No selected image'}), 400

#     try:
#         # Save uploaded image to a temp file
#         os.makedirs('static', exist_ok=True)
#         original_path = os.path.join('static', 'input.jpg')
#         file.save(original_path)

#         # Remove background
#         image_no_bg_path = remove_background(original_path)
#         if image_no_bg_path is None:
#             return jsonify({'error': 'Background removal failed'}), 500

#         # Open the processed image
#         image = Image.open(image_no_bg_path).convert('RGB')
#         image = image.resize((224, 224))
#         image_array = np.array(image)
#         image_input = np.expand_dims(image_array / 255.0, axis=0)

#         # Predict
#         predictions = model.predict(image_input)
#         predicted_index = np.argmax(predictions)
#         predicted_label = class_names[predicted_index]
#         probabilities = predictions[0].tolist()

#         # Grad-CAM
#         heatmap = grad_cam(model, tf.convert_to_tensor(image_input, dtype=tf.float32))
#         overlayed_image = overlay_heatmap(image_array, heatmap)

#         # Save heatmap image
#         heatmap_path = os.path.join('static', 'heatmap.jpg')
#         cv2.imwrite(heatmap_path, overlayed_image)

#         return jsonify({
#             'prediction': predicted_label,
#             'probabilities': probabilities,
#             'heatmap_url': heatmap_path
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # Debug: print all registered routes
# print("🔗 Registered routes:")
# print(app.url_map)

# if __name__ == '__main__':
#     app.run(debug=True)
    
    
    
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import requests
# import uuid

# app = Flask(__name__)
# CORS(app)

# # Model setup
# model_path = '1.h5'
# model = None
# try:
#     model = tf.keras.models.load_model(model_path)
#     print("✅ Model loaded.")
# except Exception as e:
#     print("❌ Model loading failed:", e)

# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# # 🧼 Background removal function using rembg API
# def remove_background(image_bytes):
#     url = "https://api.rembg.com/rmbg"
#     headers = {
#         "x-api-key": "70d943a9-621f-4107-a1e1-6d3f48901083"
#     }
#     files = {"image": ("uploaded_image.jpg", image_bytes, "image/jpeg")}
#     response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.content
#     else:
#         print("❌ Background removal failed:", response.status_code, response.text)
#         return None

# # 🔥 Grad-CAM utilities
# def grad_cam(model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
#     with tf.GradientTape() as tape:
#         conv_outputs, predictions = grad_model(image)
#         class_idx = tf.argmax(predictions[0])
#         output = predictions[:, class_idx]
#         grads = tape.gradient(output, conv_outputs)
#         pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#         conv_outputs = conv_outputs[0]
#         heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
#         heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#         return heatmap.numpy()

# def overlay_heatmap(orig_img, heatmap, alpha=0.4):
#     heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
#     return blended

# # 🔍 Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     file = request.files['image']
#     image_bytes = file.read()

#     # Step 1: Remove background
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     # Step 2: Prepare image for prediction
#     image = Image.open(io.BytesIO(cleaned_bytes)).convert('RGB')
#     image = image.resize((224, 224))
#     np_img = np.array(image)
#     input_img = np.expand_dims(np_img / 255.0, axis=0)

#     # Step 3: Predict
#     predictions = model.predict(input_img)
#     prediction_idx = np.argmax(predictions[0])
#     prediction_label = class_names[prediction_idx]
#     probabilities = predictions[0].tolist()

#     # Step 4: Grad-CAM and heatmap
#     heatmap = grad_cam(model, input_img)
#     overlay = overlay_heatmap(np_img, heatmap)

#     heatmap_filename = f"{uuid.uuid4().hex}.jpg"
#     heatmap_path = os.path.join("static", heatmap_filename)
#     os.makedirs("static", exist_ok=True)
#     cv2.imwrite(heatmap_path, overlay)

#     return jsonify({
#         'prediction': prediction_label,
#         'probabilities': probabilities,
#         'heatmap_url': f"static/{heatmap_filename}"
#     })

# # 🖼️ Serve static heatmap
# @app.route('/static/<filename>')
# def serve_heatmap(filename):
#     return send_from_directory('static', filename)


# # Debug: print all registered routes
# print("🔗 Registered routes:")
# print(app.url_map)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import requests
# import uuid

# app = Flask(__name__)
# CORS(app)

# # Create static directory if not exists
# os.makedirs("static", exist_ok=True)

# # Model setup
# model_path = '1.h5'
# model = None
# try:
#     model = tf.keras.models.load_model(model_path)
#     print("✅ Model loaded.")
# except Exception as e:
#     print("❌ Model loading failed:", e)

# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# # 🧼 Background removal function using rembg API
# def remove_background(image_bytes):
#     url = "https://api.rembg.com/rmbg"
#     headers = {
#         "x-api-key": "70d943a9-621f-4107-a1e1-6d3f48901083"
#     }
#     files = {"image": ("uploaded_image.jpg", image_bytes, "image/jpeg")}
#     response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.content
#     else:
#         print("❌ Background removal failed:", response.status_code, response.text)
#         return None

# # NEW: 🔄 Upload route for background removal only
# @app.route('/upload', methods=['POST'])
# def upload_and_remove_bg():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     image_bytes = file.read()
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     # Save cleaned image
#     output_filename = f"removed_{uuid.uuid4().hex}.png"
#     output_path = os.path.join("static", output_filename)
#     with open(output_path, "wb") as f:
#         f.write(cleaned_bytes)

#     return jsonify({
#         "removed_bg_url": f"static/{output_filename}"
#     })


# # 🔍 Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     file = request.files['image']
#     image_bytes = file.read()

#     # Step 1: Remove background
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     # Step 2: Prepare image for prediction
#     image = Image.open(io.BytesIO(cleaned_bytes)).convert('RGB')
#     image = image.resize((224, 224))
#     np_img = np.array(image)
#     input_img = np.expand_dims(np_img / 255.0, axis=0)

#     # Step 3: Predict
#     predictions = model.predict(input_img)
#     prediction_idx = np.argmax(predictions[0])
#     prediction_label = class_names[prediction_idx]
#     probabilities = predictions[0].tolist()

#     # Step 4: Grad-CAM and heatmap
#     heatmap = grad_cam(model, input_img)
#     overlay = overlay_heatmap(np_img, heatmap)

#     heatmap_filename = f"{uuid.uuid4().hex}.jpg"
#     heatmap_path = os.path.join("static", heatmap_filename)
#     cv2.imwrite(heatmap_path, overlay)

#     return jsonify({
#         'prediction': prediction_label,
#         'probabilities': probabilities,
#         'heatmap_url': f"static/{heatmap_filename}",
#         'remove_bg_url': 'static/removed_bg.png'  
        
#     })

# # 🖼️ Serve static files
# @app.route('/static/<filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # 🔥 Grad-CAM utilities
# def grad_cam(model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
#     with tf.GradientTape() as tape:
#         conv_outputs, predictions = grad_model(image)
#         class_idx = tf.argmax(predictions[0])
#         output = predictions[:, class_idx]
#         grads = tape.gradient(output, conv_outputs)
#         pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#         conv_outputs = conv_outputs[0]
#         heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
#         heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#         return heatmap.numpy()

# def overlay_heatmap(orig_img, heatmap, alpha=0.4):
#     heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
#     return blended

# # Debug: print all registered routes
# print("🔗 Registered routes:")
# print(app.url_map)

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import requests
# import uuid

# app = Flask(__name__)
# CORS(app)

# # Create static directory if not exists
# os.makedirs("static", exist_ok=True)

# # Model setup
# model_path = '1.h5'
# model = None
# try:
#     model = tf.keras.models.load_model(model_path)
#     print("✅ Model loaded.")
# except Exception as e:
#     print("❌ Model loading failed:", e)

# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# # 🧼 Background removal function using rembg API
# def remove_background(image_bytes):
#     url = "https://api.rembg.com/rmbg"
#     headers = {
#         "x-api-key": "895c0a70-1214-4511-88d0-bd35cba6bfd9"
#     }
#     files = {"image": ("uploaded_image.jpg", image_bytes, "image/jpeg")}
#     response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.content
#     else:
#         print("❌ Background removal failed:", response.status_code, response.text)
#         return None

# # 🔄 Upload route for background removal only
# @app.route('/upload', methods=['POST'])
# def upload_and_remove_bg():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     image_bytes = file.read()
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     output_filename = f"removed_{uuid.uuid4().hex}.png"
#     output_path = os.path.join("static", output_filename)
#     with open(output_path, "wb") as f:
#         f.write(cleaned_bytes)

#     return jsonify({
#         "removed_bg_url": f"static/{output_filename}"
#     })

# # 🔍 Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     file = request.files['image']
#     image_bytes = file.read()

#     # Step 1: Remove background
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     # Save background-removed image
#     remove_bg_filename = f"removed_{uuid.uuid4().hex}.png"
#     remove_bg_path = os.path.join("static", remove_bg_filename)
#     with open(remove_bg_path, "wb") as f:
#         f.write(cleaned_bytes)

#     # Step 2: Prepare image for prediction
#     image = Image.open(io.BytesIO(cleaned_bytes)).convert('RGB')
#     image = image.resize((224, 224))
#     np_img = np.array(image)
#     input_img = np.expand_dims(np_img / 255.0, axis=0)

#     # Step 3: Predict
#     predictions = model.predict(input_img)
#     prediction_idx = np.argmax(predictions[0])
#     prediction_label = class_names[prediction_idx]
#     probabilities = predictions[0].tolist()

#     # Step 4: Grad-CAM and heatmap
#     heatmap = grad_cam(model, input_img)
#     overlay = overlay_heatmap(np_img, heatmap)

#     heatmap_filename = f"{uuid.uuid4().hex}.jpg"
#     heatmap_path = os.path.join("static", heatmap_filename)
#     cv2.imwrite(heatmap_path, overlay)

#     return jsonify({
#         'prediction': prediction_label,
#         'probabilities': probabilities,
#         'heatmap_url': f"static/{heatmap_filename}",
#         "removed_bg_url": f"static/{remove_bg_filename}"
#     })

# # 🖼️ Serve static files
# @app.route('/static/<filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# # 🔥 Grad-CAM utilities
# def grad_cam(model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
#     with tf.GradientTape() as tape:
#         conv_outputs, predictions = grad_model(image)
#         class_idx = tf.argmax(predictions[0])
#         output = predictions[:, class_idx]
#         grads = tape.gradient(output, conv_outputs)
#         pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#         conv_outputs = conv_outputs[0]
#         heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
#         heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#         return heatmap.numpy()

# def overlay_heatmap(orig_img, heatmap, alpha=0.4):
#     heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
#     return blended

# # Debug: print all registered routes
# print("🔗 Registered routes:")
# print(app.url_map)

# if __name__ == '__main__':
#     app.run(debug=True)
    
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# from PIL import Image
# import io
# import os
# import cv2
# import requests
# import uuid
# import hashlib
# import random
# import datetime

# app = Flask(__name__)
# CORS(app)

# # Create static directory if not exists
# os.makedirs("static", exist_ok=True)

# # === Model loading utility ===
# def load_model_safe(path, name="Model"):
#     try:
#         model = tf.keras.models.load_model(path)
#         print(f"✅ {name} loaded from '{path}'")
#         return model
#     except Exception as e:
#         print(f"❌ {name} loading failed:", e)
#         return None

# # === Load models ===
# model = load_model_safe('1.h5', "Ripeness model")
# rambutan_model = load_model_safe('2 1.h5', "Rambutan checker model")

# class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']
# @app.route('/check-rambutan', methods=['POST'])
# def check_rambutan():
#     if rambutan_model is None:
#         return jsonify({'error': 'Rambutan model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     try:
#         file = request.files['image']
#         print(f"\n📸 New Image Uploaded: {file.filename} at {datetime.datetime.now()}")

#         # Preprocess
#         image = Image.open(file.stream).convert('RGB')
#         image = image.resize((224, 224))
#         np_img = np.array(image).astype('float32') / 255.0
#         input_img = np.expand_dims(np_img, axis=0)

#         # Predict
#         prediction = rambutan_model.predict(input_img)
#         print(f"🧠 Raw Prediction Output: {prediction}")
#         print("✅ Prediction shape:", prediction.shape)

#         # Optional: apply softmax manually (if unsure model includes it)
#         softmax_output = tf.nn.softmax(prediction[0]).numpy()
#         print(f"📊 Softmax Output: {softmax_output}")

#         predicted_class_index = int(np.argmax(softmax_output))
#         confidence = round(float(np.max(softmax_output)) * 100, 2)

#         # Match training order
#         class_labels = ['Rambutan', 'Not_Rambutan']
#         label = class_labels[predicted_class_index]

#         print(f"🔍 Predicted Index: {predicted_class_index}")
#         print(f"✅ Final Label: {label}, Confidence: {confidence}%")

#         return jsonify({
#             "label": label,
#             "confidence": confidence,
#             "raw_prediction": float(softmax_output[predicted_class_index])
#         })

#     except Exception as e:
#         print("❌ Prediction error:", str(e))
#         return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500


# # === Background Removal ===
# def remove_background(image_bytes):
#     url = "https://api.rembg.com/rmbg"
#     headers = {
#         "x-api-key": os.getenv("REMBG_API_KEY", "70d943a9-621f-4107-a1e1-6d3f48901083")  # Replace before deployment
#     }
#     files = {"image": ("uploaded_image.jpg", image_bytes, "image/jpeg")}
#     response = requests.post(url, headers=headers, files=files)

#     if response.status_code == 200:
#         return response.content
#     else:
#         print("❌ Background removal failed:", response.status_code, response.text)
#         return None

# @app.route('/upload', methods=['POST'])
# def upload_and_remove_bg():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     image_bytes = file.read()
#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     output_filename = f"removed_{uuid.uuid4().hex}.png"
#     output_path = os.path.join("static", output_filename)
#     with open(output_path, "wb") as f:
#         f.write(cleaned_bytes)

#     return jsonify({
#         "removed_bg_url": f"static/{output_filename}"
#     })

# # === Ripeness Prediction ===
# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Ripeness model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     file = request.files['image']
#     image_bytes = file.read()

#     cleaned_bytes = remove_background(io.BytesIO(image_bytes))
#     if cleaned_bytes is None:
#         return jsonify({'error': 'Background removal failed'}), 500

#     remove_bg_filename = f"removed_{uuid.uuid4().hex}.png"
#     remove_bg_path = os.path.join("static", remove_bg_filename)
#     with open(remove_bg_path, "wb") as f:
#         f.write(cleaned_bytes)

#     image = Image.open(io.BytesIO(cleaned_bytes)).convert('RGB')
#     image = image.resize((224, 224))
#     np_img = np.array(image)
#     input_img = np.expand_dims(np_img / 255.0, axis=0)

#     predictions = model.predict(input_img)
#     prediction_idx = np.argmax(predictions[0])
#     prediction_label = class_names[prediction_idx]
#     probabilities = predictions[0].tolist()

#     heatmap = grad_cam(model, input_img)
#     overlay = overlay_heatmap(np_img, heatmap)

#     heatmap_filename = f"{uuid.uuid4().hex}.jpg"
#     heatmap_path = os.path.join("static", heatmap_filename)
#     cv2.imwrite(heatmap_path, overlay)

#     return jsonify({
#         'prediction': prediction_label,
#         'probabilities': probabilities,
#         'heatmap_url': f"static/{heatmap_filename}",
#         "removed_bg_url": f"static/{remove_bg_filename}"
#     })

# @app.route('/static/<filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

# def grad_cam(model, image, layer_name="block_16_project_BN"):
#     grad_model = tf.keras.models.Model([model.inputs], [model.get_layer(layer_name).output, model.output])
#     with tf.GradientTape() as tape:
#         conv_outputs, predictions = grad_model(image)
#         class_idx = tf.argmax(predictions[0])
#         output = predictions[:, class_idx]
#         grads = tape.gradient(output, conv_outputs)
#         pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
#         conv_outputs = conv_outputs[0]
#         heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
#         heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
#         return heatmap.numpy()

# def overlay_heatmap(orig_img, heatmap, alpha=0.4):
#     heatmap = cv2.resize(heatmap, (orig_img.shape[1], orig_img.shape[0]))
#     heatmap = np.uint8(255 * heatmap)
#     heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
#     blended = cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)
#     return blended

# # === Server start ===
# print("🔗 Registered routes:")
# print(app.url_map)

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from keras.layers import TFSMLayer
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import cv2
import requests
import uuid
import hashlib
import datetime


app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'super_secret_key'  # Replace with a more secure key in production
users = {}  # In-memory user storage: {username: hashed_password}

# ========== AUTHENTICATION ROUTES ==========

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("📨 Received register data:", data)  # Debug print

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if username in users:
        return jsonify({'error': 'User already exists'}), 409

    users[username] = hash_password(password)
    print("✅ Registered users:", users)  # Debug print
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    hashed = users.get(username)
    if hashed is None or hashed != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['username'] = username
    return jsonify({'message': 'Logged in successfully'})

@app.route('/check-session')
def check_session():
    if 'user' in session:
        return jsonify({"logged_in": True, "user": session['user']})
    return jsonify({"logged_in": False})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'})

# ========== EXISTING FUNCTIONALITY BELOW ==========

os.makedirs("static", exist_ok=True)

def load_model_safe(path, name="Model"):
    try:
        model = tf.keras.models.load_model(path)
        print(f"✅ {name} loaded from '{path}'")
        return model
    except Exception as e:
        print(f"❌ {name} loading failed:", e)
        return None

model = load_model_safe('1.h5', "Ripeness model")
rambutan_model = load_model_safe('2 1.h5', "Rambutan checker model")

class_names = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe']

# @app.route('/check-rambutan', methods=['POST'])
# def check_rambutan():
#     if rambutan_model is None:
#         return jsonify({'error': 'Rambutan model not loaded.'}), 500

#     if 'image' not in request.files:
#         return jsonify({'error': 'No image file uploaded'}), 400

#     try:
#         file = request.files['image']
#         image = Image.open(file.stream).convert('RGB').resize((224, 224))
#         np_img = np.array(image).astype('float32') / 255.0
#         input_img = np.expand_dims(np_img, axis=0)

#         prediction = rambutan_model.predict(input_img)
#         softmax_output = tf.nn.softmax(prediction[0]).numpy()

#         predicted_class_index = int(np.argmax(softmax_output))
#         confidence = round(float(np.max(softmax_output)) * 100, 2)

#         class_labels = ['Not_Rambutan', 'Rambutan']
#         label = class_labels[predicted_class_index]

#         return jsonify({
#             "label": label,
#             "confidence": confidence,
#             "raw_prediction": float(softmax_output[predicted_class_index])
#         })

#     except Exception as e:
#         return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

def remove_background(image_bytes):
    url = "https://api.rembg.com/rmbg"
    headers = {
        "x-api-key": os.getenv("REMBG_API_KEY", "11861793-e96d-4fb3-8237-f55c2c375bb1")
    }
    files = {"image": ("uploaded_image.jpg", image_bytes, "image/jpeg")}
    response = requests.post(url, headers=headers, files=files)

    return response.content if response.status_code == 200 else None

@app.route('/upload', methods=['POST'])
def upload_and_remove_bg():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image_bytes = file.read()
    cleaned_bytes = remove_background(io.BytesIO(image_bytes))

    if cleaned_bytes is None:
        return jsonify({'error': 'Background removal failed'}), 500

    output_filename = f"removed_{uuid.uuid4().hex}.png"
    output_path = os.path.join("static", output_filename)
    with open(output_path, "wb") as f:
        f.write(cleaned_bytes)

    return jsonify({
        "removed_bg_url": f"static/{output_filename}"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Ripeness model not loaded.'}), 500

    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    image_bytes = file.read()

    cleaned_bytes = remove_background(io.BytesIO(image_bytes))
    if cleaned_bytes is None:
        return jsonify({'error': 'Background removal failed'}), 500

    remove_bg_filename = f"removed_{uuid.uuid4().hex}.png"
    remove_bg_path = os.path.join("static", remove_bg_filename)
    with open(remove_bg_path, "wb") as f:
        f.write(cleaned_bytes)

    image = Image.open(io.BytesIO(cleaned_bytes)).convert('RGB').resize((224, 224))
    np_img = np.array(image)
    input_img = np.expand_dims(np_img / 255.0, axis=0)

    predictions = model.predict(input_img)
    prediction_idx = np.argmax(predictions[0])
    prediction_label = class_names[prediction_idx]
    probabilities = predictions[0].tolist()

    heatmap = grad_cam(model, input_img)
    overlay = overlay_heatmap(np_img, heatmap)

    heatmap_filename = f"{uuid.uuid4().hex}.jpg"
    heatmap_path = os.path.join("static", heatmap_filename)
    cv2.imwrite(heatmap_path, overlay)

    return jsonify({
        'prediction': prediction_label,
        'probabilities': probabilities,
        'heatmap_url': f"static/{heatmap_filename}",
        "removed_bg_url": f"static/{remove_bg_filename}"
    })

@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

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
    return cv2.addWeighted(orig_img, 1 - alpha, heatmap, alpha, 0)

@app.route('/classify-rambutan-pb', methods=['POST'])
def classify_rambutan_pb():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    try:
        # Load and preprocess the image
        file = request.files['image']
        image = Image.open(file.stream).convert('RGB').resize((224, 224))
        np_img = np.array(image).astype('float32')
        input_tensor = np.expand_dims(np_img, axis=0)
        input_tensor = (input_tensor / 127.5) - 1  # normalize to [-1, 1]

        # Load the SavedModel using TFSMLayer
        model_path = "model.savedmodel"  # directory with saved_model.pb
        inference_layer = TFSMLayer(model_path, call_endpoint="serving_default")

        # Run prediction using the layer
        output_dict = inference_layer(input_tensor)

        # Get first value from dict and convert to numpy array
        prediction_tensor = list(output_dict.values())[0]
        prediction = prediction_tensor.numpy()

        # Get class index and confidence
        predicted_index = int(np.argmax(prediction))
        confidence = round(float(np.max(prediction)) * 100, 2)

        # Load class labels (e.g., 0 = not rambutan, 1 = rambutan)
        with open("labels.txt", "r") as f:
            class_names = [line.strip() for line in f.readlines()]

        label = class_names[predicted_index]

        return jsonify({
            'class_index': predicted_index,
            'label': label,
            'confidence': confidence
        })

    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

# ========== START SERVER ==========
if __name__ == '__main__':
    app.run(debug=True)