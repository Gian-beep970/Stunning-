/**
 * IMPERIAL HOUSE - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => {
        new bootstrap.Tooltip(el);
    });

    // Auto-hide alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        if (!alert.classList.contains('alert-persistent')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Handle favorite button clicks
    const favbtns = document.querySelectorAll('[data-favorite-btn]');
    favbtns.forEach(btn => {
        btn.addEventListener('click', toggleFavorite);
    });
});

/**
 * Toggle favorite status
 */
function toggleFavorite(e) {
    e.preventDefault();
    const houseId = e.currentTarget.dataset.houseId;
    
    fetch(`/api/favorite/${houseId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            e.currentTarget.innerHTML = data.message;
            e.currentTarget.classList.toggle('text-danger');
        }
    })
    .catch(error => console.error('Error:', error));
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-KE', {
        style: 'currency',
        currency: 'KES'
    }).format(amount);
}

/**
 * Load payment methods
 */
function loadPaymentMethods() {
    fetch('/api/payment-methods')
        .then(response => response.json())
        .then(data => {
            console.log('Payment methods:', data);
        });
}

/**
 * Show notification
 */
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    const alert = new bootstrap.Alert(alertDiv);
    setTimeout(() => alert.close(), 5000);
}

/**
 * Validate email
 */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

/**
 * Validate phone number
 */
function validatePhone(phone) {
    const re = /^([0-9]{10})$/;
    return re.test(phone.replace(/\D/g, ''));
}

// Export functions for use in other scripts
window.imperialHouse = {
    formatCurrency,
    loadPaymentMethods,
    showNotification,
    validateEmail,
    validatePhone
};
