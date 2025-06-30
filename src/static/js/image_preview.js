function previewImage(input, imgId) {
    const file = input.files[0];

    if (file) {
        // Validar que sea imagen
        if (!file.type.startsWith('image/')) {
            alert('Por favor selecciona un archivo de imagen válido.');
            input.value = ''; // Limpia el input
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            const img = document.getElementById(imgId);
            img.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
}
