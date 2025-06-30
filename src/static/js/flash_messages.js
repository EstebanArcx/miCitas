document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.getElementById('flash-messages');
    
    if (flashMessages) {

        // Ocultar automáticamente después de 5 segundos
        setTimeout(function () {
            flashMessages.style.opacity = '0';
            setTimeout(() => {
                flashMessages.remove();
            }, 500); // Espera que termine la transición antes de eliminar
        }, 3000);

        // Delegación de evento para botones de cerrar
        flashMessages.addEventListener('click', function (e) {
            if (e.target.classList.contains('close-flash')) {
                e.target.parentElement.remove();
            }
        });
    }
});
