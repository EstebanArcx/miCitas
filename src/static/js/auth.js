document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay parámetros de redirección en el URL
    const urlParams = new URLSearchParams(window.location.search);
    const redirectUrl = urlParams.get('redirect_url');
    
    if (redirectUrl) {
        // Mostrar mensaje de bienvenida si existe
        const flashMessages = document.querySelector('.flashes');
        if (flashMessages) {
            flashMessages.style.display = 'block';
        }
        
        // Redirigir después de 1 segundo
        setTimeout(function() {
            window.location.href = redirectUrl;
        }, 1000);
    }
});

