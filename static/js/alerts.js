// Sistema de Alertas Mejoradas
document.addEventListener('DOMContentLoaded', function() {
    initializeAlerts();
});

function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert-modern[data-auto-dismiss]');
    
    alerts.forEach(alert => {
        const duration = parseInt(alert.dataset.autoDismiss);
        const progressBar = alert.querySelector('.alert-progress');
        
        // Animar barra de progreso
        if (progressBar) {
            progressBar.style.animation = `alertProgress ${duration}ms linear`;
        }
        
        // Auto-dismiss después del tiempo especificado
        const timeoutId = setTimeout(() => {
            dismissAlert(alert);
        }, duration);
        
        // Pausar auto-dismiss al hacer hover
        alert.addEventListener('mouseenter', () => {
            clearTimeout(timeoutId);
            if (progressBar) {
                progressBar.style.animationPlayState = 'paused';
            }
        });
        
        // Reanudar auto-dismiss al quitar hover
        alert.addEventListener('mouseleave', () => {
            if (progressBar) {
                progressBar.style.animationPlayState = 'running';
            }
        });
    });
}

function dismissAlert(alert) {
    // Agregar animación de salida
    alert.style.animation = 'slideOutRight 0.3s ease-in forwards';
    
    setTimeout(() => {
        if (alert && alert.parentNode) {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }
    }, 300);
}

// Función para crear alertas dinámicamente
function showAlert(message, type = 'info', duration = 5000) {
    const alertContainer = document.querySelector('.alert-container') || createAlertContainer();
    
    const iconMap = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-triangle',
        'danger': 'fas fa-exclamation-triangle',
        'warning': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    };
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show alert-modern" role="alert" data-auto-dismiss="${duration}">
            <div class="alert-content">
                <div class="alert-icon">
                    <i class="${iconMap[type] || iconMap.info}"></i>
                </div>
                <div class="alert-message">${message}</div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            <div class="alert-progress"></div>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    // Inicializar la nueva alerta
    const newAlert = alertContainer.lastElementChild;
    initializeSingleAlert(newAlert);
}

function createAlertContainer() {
    const container = document.createElement('div');
    container.className = 'alert-container';
    document.body.appendChild(container);
    return container;
}

function initializeSingleAlert(alert) {
    const duration = parseInt(alert.dataset.autoDismiss);
    const progressBar = alert.querySelector('.alert-progress');
    
    if (progressBar) {
        progressBar.style.animation = `alertProgress ${duration}ms linear`;
    }
    
    const timeoutId = setTimeout(() => {
        dismissAlert(alert);
    }, duration);
    
    alert.addEventListener('mouseenter', () => {
        clearTimeout(timeoutId);
        if (progressBar) {
            progressBar.style.animationPlayState = 'paused';
        }
    });
    
    alert.addEventListener('mouseleave', () => {
        if (progressBar) {
            progressBar.style.animationPlayState = 'running';
        }
    });
}

// Exponer función globalmente para uso en otros scripts
window.showAlert = showAlert;