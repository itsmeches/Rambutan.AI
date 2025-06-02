document.addEventListener('DOMContentLoaded', () => {
  // Navbar and dark mode
  const darkToggle = document.getElementById('darkToggle');
  if (darkToggle) {
    darkToggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('theme', 'dark');
        darkToggle.innerText = '☀️';
      } else {
        localStorage.setItem('theme', 'light');
        darkToggle.innerText = '🌙';
      }
    });
    // On load, restore preference
    if (localStorage.getItem('theme') === 'dark') {
      document.body.classList.add('dark-mode');
      darkToggle.innerText = '☀️';
    } else {
      darkToggle.innerText = '🌙';
    }
  }

  // Mobile menu
  const mobileMenu = document.getElementById('mobile-menu');
  const navLinks = document.getElementById('nav-links');
  if (mobileMenu && navLinks) {
    mobileMenu.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }

  // Only run the following if on index.html (where these elements exist)
  const imageUpload = document.getElementById('imageUpload');
  const uploadedImage = document.getElementById('uploadedImage');
  const cleanedPreview = document.getElementById('cleanedPreview');
  const cropBtn = document.getElementById('cropBtn');
  const removeBtn = document.getElementById('removeBtn');
  const result = document.getElementById('result');
  const heatmapPreview = document.getElementById('heatmapPreview');
  const heatmapImg = document.getElementById('heatmapImg');
  const toggleHeatmapBtn = document.getElementById('toggleHeatmap');
  const aiInsight = document.getElementById('aiInsight');

  let cropper;
  let croppedBlob = null;

  if (imageUpload && uploadedImage && cropBtn && cleanedPreview && removeBtn && result && heatmapPreview && heatmapImg && toggleHeatmapBtn && aiInsight) {
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

    cropBtn.addEventListener('click', () => {
      if (!cropper) return;

      cropBtn.disabled = true;

      const canvas = cropper.getCroppedCanvas({
        width: 300,
        height: 300
      });

      canvas.toBlob(blob => {
        croppedBlob = blob;
        classifyImage();
      }, 'image/jpeg');
    });

    async function classifyImage() {
      if (!croppedBlob) {
        alert('Please crop the image first.');
        return;
      }

      result.textContent = '🔍 Removing background and classifying...';
      cropBtn.disabled = true;

      try {
        const uploadForm = new FormData();
        uploadForm.append('file', croppedBlob, 'cropped.jpg');

        const removeRes = await fetch('http://localhost:5000/upload', {
          method: 'POST',
          body: uploadForm
        });

        const removeData = await removeRes.json();

        if (!removeData.removed_bg_url) {
          throw new Error('No background removed image returned');
        }

        const imageUrl = `http://localhost:5000/${removeData.removed_bg_url}`;
        cleanedPreview.src = `${imageUrl}?t=${Date.now()}`;
        cleanedPreview.classList.remove('hidden');

        const removedImgResponse = await fetch(imageUrl);
        const removedBlob = await removedImgResponse.blob();

        const predictForm = new FormData();
        predictForm.append('image', removedBlob, 'cleaned.jpg');

        const predictRes = await fetch('http://localhost:5000/predict', {
          method: 'POST',
          body: predictForm
        });

        const data = await predictRes.json();

        if (data.prediction) {
          result.innerHTML = `✅ Prediction: <strong>${data.prediction}</strong>`;
        }

        if (Array.isArray(data.probabilities)) {
          updateSlidersAndInsights(data.probabilities);
        }

        if (data.heatmap_url) {
          heatmapImg.src = `http://localhost:5000/${data.heatmap_url}?t=${Date.now()}`;
          heatmapPreview.classList.remove('hidden');
        } else {
          console.error('No heatmap returned.');
        }

        result.scrollIntoView({ behavior: 'smooth', block: 'center' });

      } catch (err) {
        console.error(err);
        result.textContent = '❌ Failed to classify image.';
      }

      cropBtn.disabled = false;
    }

    toggleHeatmapBtn.addEventListener('click', () => {
      heatmapPreview.classList.toggle('hidden');
    });

    removeBtn.addEventListener('click', resetAll);

    function resetAll() {
      croppedBlob = null;
      imageUpload.value = '';
      uploadedImage.src = '';
      uploadedImage.classList.add('hidden');
      cleanedPreview.src = '';
      cleanedPreview.classList.add('hidden');
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

      cropBtn.disabled = false;
    }

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
  }
});