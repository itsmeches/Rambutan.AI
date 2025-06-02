# 🍈 RambutanAI

A web-based tool for **Leaf-Based Bitter Gourd Health Assessment** using a **Convolutional Neural Network (CNN)** model to detect **NPK Deficiencies** and assess **Soil Compatibility** from uploaded leaf images.

This project is built using **Flask (Python)** for backend processing and **HTML/CSS/JS + Cropper.js** for the frontend.

---

## 📁 Project Structure

```
rambutanai/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── cropper.min.js
├── model/
│   └── cnn_model.h5
├── uploads/
├── requirements.txt
└── README.md
```

---

## 🛠️ Prerequisites

### ✅ 1. Install Python (3.10+)

- Download from: https://www.python.org/downloads/
- During installation, **check "Add Python to PATH"**

---

### ✅ 2. Browser

Any modern browser (Chrome recommended).

---

### ✅ 3. Code Editor (Optional but Recommended)

- Download VS Code: https://code.visualstudio.com/
- Install the extension **Live Server** to test frontend alone.

---

## 📦 Python Dependencies

Install these by running:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
flask
flask-cors
tensorflow
numpy
Pillow
opencv-python
requests
```

---

## 🚀 How to Run the Project

### 📅 Step 1: Download the Project

You can:
- Download as `.zip` and extract it
- OR clone via Git:

```bash
git clone https://github.com/yourusername/rambutanai.git
cd rambutanai
```

---

### 🐍 Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

---

### ▶️ Step 3: Run the Flask Server

```bash
python app.py
```

You should see output like:

```
 * Running on http://127.0.0.1:5000/
```

---

### 🌱 Step 4: Use the Web App

1. Open your browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Upload or crop a bitter gourd leaf.
3. View the model prediction (NPK deficiency/soil compatibility).

---

## 💻 Tech Stack

### Frontend:
- HTML, CSS, JavaScript
- Cropper.js

### Backend:
- Flask (Python)
- TensorFlow (ML)
- OpenCV (Image Preprocessing)
- Pillow (Image Conversion)
- UUID, Requests, Hashlib for Utilities

---

## ❓ FAQs

**Q: I get an error about a missing model file?**  
A: Make sure `cnn_model.h5` is placed inside the `model/` folder.

**Q: The browser doesn’t open automatically?**  
A: Manually open a browser and go to: http://127.0.0.1:5000/

---

## 👤 Author

Developed by **Chester Andaya**  
📧 Email: chester.andaya11@gmail.com

---