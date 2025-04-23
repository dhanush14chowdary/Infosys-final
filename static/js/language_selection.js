// Show tooltip on language input focus
const languageInput = document.getElementById('language');
const tooltip = document.getElementById('language-tooltip');

languageInput.addEventListener('focus', () => {
    tooltip.style.opacity = '1';
    tooltip.style.visibility = 'visible';
});

languageInput.addEventListener('blur', () => {
    tooltip.style.opacity = '0';
    tooltip.style.visibility = 'hidden';
});

// Get references to the form, progress container, and progress bar
const form = document.getElementById('language-form');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');

// Listen for form submission
form.addEventListener('submit', function(event) {
    // Show progress bar when the form is submitted
    progressContainer.style.display = 'block';
    let progress = 0;
    progressBar.value = progress;

    // Simulate progress bar update
    const interval = setInterval(() => {
        progress += 10;
        progressBar.value = progress;
        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 500); // Simulate a 5-second process
});


// // Confirm submission
// const form = document.querySelector('form');
// form.addEventListener('submit', () => {
//     alert('Your language selection has been submitted!');
// });
