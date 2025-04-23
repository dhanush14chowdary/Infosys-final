// Show tooltip on file input focus
const fileInput = document.getElementById('video_file');
const tooltip = document.getElementById('file-tooltip');

fileInput.addEventListener('focus', () => {
    tooltip.style.opacity = '1';
    tooltip.style.visibility = 'visible';
});

fileInput.addEventListener('blur', () => {
    tooltip.style.opacity = '0';
    tooltip.style.visibility = 'hidden';
});

// Simulate progress bar while allowing actual form submission
const form = document.querySelector('form');
const progressBar = document.querySelector('.progress');

form.addEventListener('submit', (e) => {
    progressBar.style.width = '0%';
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width += 5;
            progressBar.style.width = width + '%';
        }
    }, 100);
    // Allow form submission to proceed naturally
});
