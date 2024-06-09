$(document).ready(function() {
    $('.container').hide().fadeIn(1200);  // 1000 milliseconds = 1 second
});



document.getElementById('homeButton').addEventListener('click', function(event) {
    event.preventDefault();
    alert('Redirecting to Home Page');
    window.location.href = '/';
});

document.getElementById('menuButton').addEventListener('click', function(event) {
    event.preventDefault();
    alert('Redirecting to Menu Page');
    window.location.href = '/menu';
});

