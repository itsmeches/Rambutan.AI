const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const classifyBtn = document.getElementById('classifyBtn');
const removeBtn = document.getElementById('removeBtn');
const resultDiv = document.getElementById('result');
const heatmapImg = document.getElementById('heatmapImg');
const heatmapPreview = document.getElementById('heatmapPreview');
const toggleHeatmapBtn = document.getElementById('toggleHeatmap');
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.getElementById('nav-links');
const aiInsight = document.getElementById('aiInsight');

let selectedFile = null;

// 🍔 Toggle mobile menu
mobileMenu?.addEventListener('click', () => {
  navLinks?.classList.toggle('show');
});

// 📸 Handle image preview
imageUpload?.addEventListener('change', () => {
  selectedFile = imageUpload.files?.[0];

  if (selectedFile) {
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.innerHTML = `<img src="${reader.result}" alt="Preview" />`;
    };
    reader.readAsDataURL(selectedFile);
  } else {
    resetPreview();
  }
});

// 🧠 Handle image classification
classifyBtn?.addEventListener('click', async () => {
  if (!selectedFile) {
    alert('Please upload an image first.');
    return;
  }

  resultDiv.innerHTML = '🔍 Classifying...';

  try {
    const formData = new FormData();
    formData.append('image', selectedFile);

    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData
    });

    const data = await res.json();

    if (data.prediction) {
      resultDiv.innerHTML = `✅ Prediction: <strong>${data.prediction}</strong>`;
    }

    if (Array.isArray(data.probabilities)) {
      updateSlidersAndInsights(data.probabilities);
    }

    if (data.heatmap_url) {
      heatmapImg.src = `http://localhost:5000/${data.heatmap_url}?t=${Date.now()}`;
    } else {
      console.error('No heatmap returned.');
    }
  } catch (err) {
    console.error(err);
    resultDiv.innerHTML = '❌ Failed to classify image.';
  }
});

// 🔥 Toggle heatmap visibility
toggleHeatmapBtn?.addEventListener('click', () => {
  heatmapPreview?.classList.toggle('hidden');
});

// ❌ Remove/reset inputs
removeBtn?.addEventListener('click', resetAll);

// 🔁 Reset all UI elements
function resetAll() {
  selectedFile = null;
  imageUpload.value = '';
  resetPreview();
  resultDiv.innerHTML = 'Prediction will appear here.';
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
}

// 🔍 Reset preview
function resetPreview() {
  imagePreview.innerHTML = '<span>No image selected</span>';
}

// 📊 Update sliders and AI insight
function updateSlidersAndInsights(probabilities) {
  const classMap = {
    Rotten: 'rottenSlider',
    Ripe: 'ripeSlider',
    Raw: 'rawSlider',
    Towards_Decay: 'towardsdecaySlider',
    Towards_Ripe: 'towardsripeSlider'
  };

  Object.entries(classMap).forEach(([label, id], index) => {
    const percent = Math.round(probabilities[index] * 100);
    const slider = document.getElementById(id);
    if (slider) {
      slider.value = percent;
      const labelElem = slider.previousElementSibling;
      if (labelElem) {
        labelElem.innerText = `${label.replace('_', ' ')}: ${percent}%`;
      }
    }
  });

  const maxIndex = probabilities.indexOf(Math.max(...probabilities));
  const bestLabel = Object.keys(classMap)[maxIndex];
  const confidence = Math.round(probabilities[maxIndex] * 100);

  aiInsight.innerHTML = `<strong>AI Insight:</strong> Most likely <strong>${bestLabel.replace('_', ' ')}</strong> with <strong>${confidence}%</strong> confidence.`;
}
