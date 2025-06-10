# 🍈 RambutanAI

A web-based tool for **Rambutan Fruit Classification** using a **Convolutional Neural Network (CNN)** model to detect **whether the uploaded image is a Rambutan or not** and assess **its condition** based on visual input.

Built using **Flask (Python)** for backend processing and **HTML/CSS/JS** for the frontend.

---

## ⚖️ Ethical Use & Creative Encouragement

> This project was developed as a reference and learning tool for understanding image classification with CNNs, image preprocessing, and web integration.

You're welcome to **study**, **fork**, and **learn from** this code—but please avoid copying it directly for submissions or evaluations. Instead, consider it a **starting point** to build and improve upon with your own features, models, or approaches.

Here are a few ideas to make it your own:
- Try different CNN architectures
- Customize the frontend UX or UI
- Enhance the classification logic
- Add new features like bounding box or severity analysis

Let's grow **together as developers**, not just repeat code.

---

## 📁 Project Structure
...

```
rambutanai/
├── app.py
├── Front-End/
│   └── index.html
│   └── how-to-use.html
│   └── about.html
│   └── contact.html
│   ├── style.css
│   ├── script.js
├── static/
    ├──upload folder
├── model/
│   └── 1.h5
│   ├── 2.h5
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
flask flask-login flask-sqlalchemy
flask-login
flask-sqlalchemy
flask flask-login flask-sqlalchemy
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
2. Upload or crop a Rambutan fruit.
3. View the model prediction (Rambutan).

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

Developed by **Chester Andaya, Niccollo Dayritt, Psalm Ashley Andal**  
📧 Email: chester.andaya11@gmail.com

---
