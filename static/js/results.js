// results.js

// You can add any interactivity here, if needed. 
// For now, let's ensure that the video is fully loaded before showing any messages if desired.

// For example, you could add an alert or custom action after the video ends:

document.querySelector('video').addEventListener('ended', function() {
    alert('Video playback finished!');
});
