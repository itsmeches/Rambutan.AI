document.addEventListener("DOMContentLoaded", function () {
  const imageUpload = document.getElementById("imageUpload");
  const imagePreview = document.getElementById("imagePreview");
  const classifyBtn = document.getElementById("classifyBtn");
  const removeBtn = document.getElementById("removeBtn");
  const toggleHeatmap = document.getElementById("toggleHeatmap");
  const heatmapImg = document.getElementById("heatmapImg");
  const result = document.getElementById("result");
  const aiInsight = document.getElementById("aiInsight");
  const rottenSlider = document.getElementById("rottenSlider");
  const decaySlider = document.getElementById("decaySlider");
  const mobileMenu = document.getElementById("mobile-menu");
  const navLinks = document.getElementById("nav-links");

  imageUpload.addEventListener("change", () => {
    const file = imageUpload.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        imagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" />`;
      };
      reader.readAsDataURL(file);
    } else {
      imagePreview.innerHTML = "<span>No image selected</span>";
    }
  });

  classifyBtn.addEventListener("click", () => {
    result.textContent = "Predicted: Early Decay";
    rottenSlider.value = 70;
    decaySlider.value = 60;
    aiInsight.innerHTML = "<strong>AI Insight:</strong> This rambutan is entering decay stage.";
  });

  removeBtn.addEventListener("click", () => {
    imageUpload.value = "";
    imagePreview.innerHTML = "<span>No image selected</span>";
    result.textContent = "Prediction will appear here.";
    rottenSlider.value = 50;
    decaySlider.value = 40;
    aiInsight.innerHTML = "<strong>AI Insight:</strong> This rambutan is likely in the early stage of decay.";
  });

  toggleHeatmap.addEventListener("click", () => {
    heatmapImg.style.display = heatmapImg.style.display === "none" ? "block" : "none";
  });

  mobileMenu.addEventListener("click", () => {
    navLinks.classList.toggle("show");
  });
});
