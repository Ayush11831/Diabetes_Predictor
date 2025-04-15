document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('diabetesForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = form.querySelector('.submit-btn');
            const loadingSpinner = document.createElement('div');
            loadingSpinner.className = 'loading-spinner';
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '';
            submitBtn.appendChild(loadingSpinner);
            
            // Collect form data
            const formData = {
                pregnancies: form.querySelector('[name="pregnancies"]').value,
                glucose: form.querySelector('[name="glucose"]').value,
                bloodPressure: form.querySelector('[name="bloodPressure"]').value,
                skinThickness: form.querySelector('[name="skinThickness"]').value,
                insulin: form.querySelector('[name="insulin"]').value,
                bmi: form.querySelector('[name="bmi"]').value,
                diabetesPedigree: form.querySelector('[name="diabetesPedigree"]').value,
                age: form.querySelector('[name="age"]').value,
                frequentUrination: form.querySelector('[name="frequentUrination"]:checked')?.value || 'no',
                excessiveThirst: form.querySelector('[name="excessiveThirst"]:checked')?.value || 'no',
                hunger: form.querySelector('[name="hunger"]:checked')?.value || 'no',
                fatigue: form.querySelector('[name="fatigue"]:checked')?.value || 'no',
                blurredVision: form.querySelector('[name="blurredVision"]:checked')?.value || 'no',
                slowHealing: form.querySelector('[name="slowHealing"]:checked')?.value || 'no',
                tinglingNumbness: form.querySelector('[name="tinglingNumbness"]:checked')?.value || 'no'
            };
            
            // Get current language
            const urlParams = new URLSearchParams(window.location.search);
            const lang = urlParams.get('lang') || 'en';
            
            // Send to server
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                // Redirect to results page with language parameter
                window.location.href = `/results?lang=${lang}`;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Calculate Risk';
            });
        });
    }
    
    // Animate risk meter on results page
    const riskLevel = document.querySelector('.risk-level');
    if (riskLevel) {
        // Get the risk percentage from the style attribute
        const width = riskLevel.style.width;
        riskLevel.style.width = '0';
        
        // Trigger the animation after a short delay
        setTimeout(() => {
            riskLevel.style.width = width;
        }, 300);
    }
    
    // Animate gauge chart
    const gaugeFill = document.querySelector('.gauge-fill');
    if (gaugeFill) {
        // Get the risk percentage from the data attribute
        const riskPercentage = parseFloat(document.querySelector('.gauge-cover').textContent);
        const rotation = riskPercentage / 100 * 0.5;
        
        gaugeFill.style.transform = 'rotate(0.25turn)';
        
        setTimeout(() => {
            gaugeFill.style.transform = `rotate(${0.25 + rotation}turn)`;
        }, 300);
    }
    
    // Language selector functionality
    const languageBtns = document.querySelectorAll('.language-btn');
    languageBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.dataset.lang;
            const currentUrl = new URL(window.location.href);
            
            if (lang === 'en') {
                currentUrl.searchParams.delete('lang');
            } else {
                currentUrl.searchParams.set('lang', lang);
            }
            
            window.location.href = currentUrl.toString();
        });
    });
    
    // Mark current language as active
    const urlParams = new URLSearchParams(window.location.search);
    const currentLang = urlParams.get('lang') || 'en';
    
    document.querySelectorAll(`.language-btn[data-lang="${currentLang}"]`).forEach(btn => {
        btn.classList.add('active');
    });
    
    // Add animations to elements
    const animateElements = document.querySelectorAll('.result-card, .container, .welcome-card');
    animateElements.forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.animationDelay = `${index * 0.1}s`;
    });
});



// Health Tips Carousel
document.addEventListener('DOMContentLoaded', function() {
    const tips = document.querySelectorAll('.tip');
    const dots = document.querySelectorAll('.tip-dot');
    let currentTip = 0;
    
    // Show initial tip
    showTip(currentTip);
    
    // Auto-rotate tips every 5 seconds
    const tipInterval = setInterval(nextTip, 5000);
    
    // Dot click event
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            clearInterval(tipInterval);
            currentTip = parseInt(this.dataset.index);
            showTip(currentTip);
        });
    });
    
    function showTip(index) {
        // Hide all tips and remove active class from dots
        tips.forEach(tip => tip.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        // Show selected tip and activate corresponding dot
        tips[index].classList.add('active');
        dots[index].classList.add('active');
    }
    
    function nextTip() {
        currentTip = (currentTip + 1) % tips.length;
        showTip(currentTip);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Update slider value displays
    const sliders = document.querySelectorAll('.symptom-slider');
    sliders.forEach(slider => {
        const valueDisplay = slider.nextElementSibling;
        valueDisplay.textContent = slider.value;
        
        slider.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
        });
    });

    const form = document.getElementById('diabetesForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Show loading state
            const submitBtn = form.querySelector('.submit-btn');
            const loadingSpinner = document.createElement('div');
            loadingSpinner.className = 'loading-spinner';
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '';
            submitBtn.appendChild(loadingSpinner);
            
            // Collect form data
            const formData = {
                pregnancies: form.querySelector('[name="pregnancies"]').value,
                glucose: form.querySelector('[name="glucose"]').value,
                bloodPressure: form.querySelector('[name="bloodPressure"]').value,
                skinThickness: form.querySelector('[name="skinThickness"]').value,
                insulin: form.querySelector('[name="insulin"]').value,
                bmi: form.querySelector('[name="bmi"]').value,
                diabetesPedigree: form.querySelector('[name="diabetesPedigree"]').value,
                age: form.querySelector('[name="age"]').value,
                frequentUrination: form.querySelector('[name="frequentUrination"]').value,
                excessiveThirst: form.querySelector('[name="excessiveThirst"]').value,
                hunger: form.querySelector('[name="hunger"]').value,
                fatigue: form.querySelector('[name="fatigue"]').value,
                blurredVision: form.querySelector('[name="blurredVision"]').value,
                slowHealing: form.querySelector('[name="slowHealing"]').value,
                tinglingNumbness: form.querySelector('[name="tinglingNumbness"]').value
            };
            
            // Rest of your existing form submission code...
            // Get current language
            const urlParams = new URLSearchParams(window.location.search);
            const lang = urlParams.get('lang') || 'en';
            
            // Send to server
            fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                // Redirect to results page with language parameter
                window.location.href = `/results?lang=${lang}`;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error: ' + error.message);
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Calculate Risk';
            });
        });
    }
    
    // Rest of your existing JavaScript...
});
