// Function to show the custom alert with a dynamic message
function showCustomAlert(message, id) {
    const alertBox = document.getElementById('cool-alert');
    const overlay = document.getElementById('background-overlay');
    
    // Set the custom message in the alert
    alertBox.querySelector('p').innerText = message;
    
    // Make the background overlay and the alert visible
    overlay.style.visibility = 'visible';
    overlay.style.opacity = '1';
    alertBox.classList.add('show'); // Show the alert
    
    // Set the confirm and cancel actions for the alert buttons
    document.getElementById('accept-btn').onclick = function() {
        window.location.href = `/delete_event/${id}`; // Confirm function
        hideCustomAlert(); // Hide the alert
    };
    document.getElementById('dismiss-btn').onclick = function() {
        hideCustomAlert(); // Hide the alert
    };
}

// Function to hide the custom alert
function hideCustomAlert() {
    const alertBox = document.getElementById('cool-alert');
    const overlay = document.getElementById('background-overlay');
    
    // Hide the background overlay and alert
    overlay.style.visibility = 'hidden';
    overlay.style.opacity = '0';
    alertBox.classList.remove('show'); // Hide the alert
}

// Function to confirm the deletion
function confirmDelete(id, title) {
    const message = `Sei sicuro di voler eliminare l'evento "${title}"?`;

    showCustomAlert(message, id);
}
