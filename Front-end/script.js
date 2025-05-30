const imageUpload = document.getElementById('imageUpload');
const uploadedImage = document.getElementById('uploadedImage');
const croppedPreview = document.getElementById('croppedPreview');
const cropBtn = document.getElementById('cropBtn');
const classifyBtn = document.getElementById('classifyBtn');
const removeBtn = document.getElementById('removeBtn');
const result = document.getElementById('result');
const heatmapPreview = document.getElementById('heatmapPreview'); // ✅ FIXED
const heatmapImg = document.getElementById('heatmapImg');
const toggleHeatmapBtn = document.getElementById('toggleHeatmap');
const aiInsight = document.getElementById('aiInsight');
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.getElementById('nav-links');

let cropper;
let croppedBlob = null;

// 🍔 Toggle mobile menu
mobileMenu?.addEventListener('click', () => {
  navLinks?.classList.toggle('show');
});

// 📸 Handle image upload and initialize Cropper.js
imageUpload.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    uploadedImage.src = reader.result;
    uploadedImage.classList.remove('hidden');

    if (cropper) cropper.destroy();
    cropper = new Cropper(uploadedImage, {
      aspectRatio: 1,
      viewMode: 1
    });
  };
  reader.readAsDataURL(file);
});

// ✂️ Crop the image and show the cropped preview
cropBtn.addEventListener('click', () => {
  if (!cropper) return;

  const canvas = cropper.getCroppedCanvas({
    width: 300,
    height: 300
  });

  canvas.toBlob(blob => {
    croppedBlob = blob;

    const dataUrl = canvas.toDataURL();
    croppedPreview.src = dataUrl;
    croppedPreview.classList.remove('hidden');
  }, 'image/jpeg');
});

// 🧠 Classify the cropped image
classifyBtn.addEventListener('click', async () => {
  if (!croppedBlob) {
    alert('Please crop the image first.');
    return;
  }

  result.textContent = '🔍 Classifying...';

  try {
    const formData = new FormData();
    formData.append('image', croppedBlob, 'cropped.jpg');

    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    if (data.prediction) {
      result.innerHTML = `✅ Prediction: <strong>${data.prediction}</strong>`;
    }

    if (Array.isArray(data.probabilities)) {
      updateSlidersAndInsights(data.probabilities);
    }

    if (data.heatmap_url) {
      heatmapImg.src = `http://localhost:5000/${data.heatmap_url}?t=${Date.now()}`;
      heatmapPreview.classList.remove('hidden'); // ✅ FIXED
    } else {
      console.error('No heatmap returned.');
    }

  } catch (err) {
    console.error(err);
    result.textContent = '❌ Failed to classify image.';
  }
});

// 🔥 Toggle heatmap visibility
toggleHeatmapBtn?.addEventListener('click', () => {
  heatmapPreview?.classList.toggle('hidden'); // ✅ FIXED
});

// ❌ Remove/reset inputs
removeBtn?.addEventListener('click', resetAll);

// 🔁 Reset all UI elements
function resetAll() {
  croppedBlob = null;
  imageUpload.value = '';
  uploadedImage.src = '';
  uploadedImage.classList.add('hidden');
  croppedPreview.src = '';
  croppedPreview.classList.add('hidden');
  result.innerHTML = 'Prediction will appear here.';
  heatmapImg.src = 'placeholder-heatmap.png';
  heatmapPreview.classList.add('hidden'); 
  aiInsight.innerHTML = '<strong>AI Insight:</strong> Awaiting classification...';

  const sliderIDs = ['rottenSlider', 'ripeSlider', 'rawSlider', 'towardsdecaySlider', 'towardsripeSlider'];
  sliderIDs.forEach(id => {
    const slider = document.getElementById(id);
    if (slider) {
      slider.value = 0;
      const label = slider.previousElementSibling;
      if (label) label.innerText = label.innerText.split(':')[0] + ': 0%';
    }
  });

  if (cropper) {
    cropper.destroy();
    cropper = null;
  }
}

// 📊 Update sliders and AI insight
function updateSlidersAndInsights(probabilities) {
  const classMap = {
    Rotten: ['rottenSlider', 'rottenLabel'],
    Ripe: ['ripeSlider', 'ripeLabel'],
    Raw: ['rawSlider', 'rawLabel'],
    Towards_Decay: ['towardsdecaySlider', 'towardsdecayLabel'],
    Towards_Ripe: ['towardsripeSlider', 'towardsripeLabel']
  };

  Object.entries(classMap).forEach(([label, [sliderId, labelId]], index) => {
    const percent = Math.round(probabilities[index] * 100);
    const slider = document.getElementById(sliderId);
    const labelElem = document.getElementById(labelId);
    if (slider && labelElem) {
      slider.value = percent;
      labelElem.innerText = `${label.replace('_', ' ')}: ${percent}%`;
    }
  });

  const maxIndex = probabilities.indexOf(Math.max(...probabilities));
  const bestLabel = Object.keys(classMap)[maxIndex];
  const confidence = Math.round(probabilities[maxIndex] * 100);

  aiInsight.innerHTML = `<strong>AI Insight:</strong> Most likely <strong>${bestLabel.replace('_', ' ')}</strong> with <strong>${confidence}%</strong> confidence.`;
}

