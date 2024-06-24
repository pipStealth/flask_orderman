document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.content').classList.add('visible');
});
function toggleMode() {
    const body = document.body;
    const currentMode = body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode';
    const newMode = currentMode === 'dark-mode' ? 'light-mode' : 'dark-mode';
    const icon = document.getElementById('mode-toggle-icon');

    body.classList.remove(currentMode);
    body.classList.add(newMode);

    // Update the icon
    if (newMode === 'dark-mode') {
        icon.src = '../static/img/darkmode.png';
    } else {
        icon.src = '../static/img/lightmode.png';
    }

    // Save the mode in localStorage
    localStorage.setItem('mode', newMode);
}

// Initialize mode based on localStorage
document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('mode') || 'light-mode';
    const body = document.body;
    const icon = document.getElementById('mode-toggle-icon');
    
    body.classList.add(savedMode);

    // Set the correct icon
    if (savedMode === 'dark-mode') {
        icon.src = '../static/img/darkmode.png';
    } else {
        icon.src = '../static/img/lightmode.png';
    }
});

// Add this to your index.js
function purchaseItem(itemId) {
    // Implement the purchase logic here
    // For example, you can send an AJAX request to your backend to handle the purchase
    alert('Item with ID ' + itemId + ' purchased!');
}
