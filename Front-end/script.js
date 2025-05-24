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

let selectedFile = null;

// Mobile navbar toggle
mobileMenu.addEventListener('click', () => {
  navLinks.classList.toggle('show');
});

// Image preview
imageUpload.addEventListener('change', () => {
  selectedFile = imageUpload.files[0];

  if (selectedFile) {
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.innerHTML = `<img src="${reader.result}" alt="Preview" />`;
    };
    reader.readAsDataURL(selectedFile);
  } else {
    imagePreview.innerHTML = '<span>No image selected</span>';
  }
});

// Classification and Grad-CAM request
classifyBtn.addEventListener('click', () => {
  if (!selectedFile) {
    alert('Please upload an image first.');
    return;
  }

  resultDiv.innerHTML = '🔍 Classifying...';

  const formData = new FormData();
  formData.append('image', selectedFile);

  fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.prediction) {
        resultDiv.innerHTML = `✅ Prediction: <strong>${data.prediction}</strong>`;
      }

      if (data.probabilities) {
        updateSlidersAndInsights(data.probabilities);
      }

      if (data.heatmap_url) {
        heatmapImg.src = `http://localhost:5000/${data.heatmap_url}?t=${new Date().getTime()}`;
      } else {
        console.error('No heatmap returned from backend.');
      }
    })
    .catch(err => {
      console.error(err);
      resultDiv.innerHTML = '❌ Failed to classify image.';
    });
});

// Toggle heatmap visibility
toggleHeatmapBtn.addEventListener('click', () => {
  heatmapPreview.classList.toggle('hidden');
});

// Clear inputs
removeBtn.addEventListener('click', () => {
  selectedFile = null;
  imageUpload.value = '';
  imagePreview.innerHTML = '<span>No image selected</span>';
  resultDiv.innerHTML = 'Prediction will appear here.';
  heatmapImg.src = 'placeholder-heatmap.png';
  heatmapPreview.classList.add('hidden');

  // Reset sliders and insight
  ['rottenSlider', 'ripeSlider', 'rawSlider', 'towardsdecaySlider', 'towardsripeSlider'].forEach(id => {
    const slider = document.getElementById(id);
    if (slider) slider.value = 0;

    const label = slider?.previousElementSibling;
    if (label) label.innerText = label.innerText.split(':')[0] + ': 0%';
  });

  document.getElementById("aiInsight").innerHTML = '<strong>AI Insight:</strong> Awaiting classification...';
});

// Function to update sliders and confidence levels
function updateSlidersAndInsights(probabilities) {
  const classNames = ['Rotten', 'Ripe', 'Raw', 'Towards_Decay', 'Towards_Ripe'];

  const sliders = {
    'Rotten': document.getElementById('rottenSlider'),
    'Ripe': document.getElementById('ripeSlider'),
    'Raw': document.getElementById('rawSlider'),
    'Towards_Decay': document.getElementById('towardsdecaySlider'),
    'Towards_Ripe': document.getElementById('towardsripeSlider'),
  };

  classNames.forEach((label, i) => {
    const percent = Math.round(probabilities[i] * 100);
    const slider = sliders[label];
    if (slider) {
      slider.value = percent;
      const labelElem = slider.previousElementSibling;
      if (labelElem) {
        labelElem.innerText = `${label.replace('_', ' ')}: ${percent}%`;
      }
    }
  });

  // Show insight
  const maxIndex = probabilities.indexOf(Math.max(...probabilities));
  const predictedLabel = classNames[maxIndex];
  const confidence = Math.round(probabilities[maxIndex] * 100);
  document.getElementById("aiInsight").innerHTML = `<strong>AI Insight:</strong> Most likely <strong>${predictedLabel.replace('_', ' ')}</strong> with <strong>${confidence}%</strong> confidence.`;
}
