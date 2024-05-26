

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