document.addEventListener('DOMContentLoaded', function () {
    const fechaInput = document.getElementById('fecha');
    const horaSelect = document.getElementById('hora');

    if (fechaInput) {
        fechaInput.addEventListener('change', function () {
            const fecha = this.value;
            horaSelect.innerHTML = '<option value="">Cargando horas...</option>';

            fetch(`/user_panel/get_available_hours/${serviceId}?fecha=${fecha}`)
                .then(response => response.json())
                .then(data => {
                    horaSelect.innerHTML = '';
                    if (data.length === 0) {
                        horaSelect.innerHTML = '<option value="">Sin horas disponibles</option>';
                    } else {
                        data.forEach(hora => {
                            horaSelect.innerHTML += `<option value="${hora}">${hora}</option>`;
                        });
                    }
                })
                .catch(err => {
                    console.error(err);
                    horaSelect.innerHTML = '<option value="">Error al cargar horas</option>';
                });
        });
    }
});

// Asignar dinámicamente el id del servicio al script
const serviceId = parseInt(window.location.pathname.split('/').pop());
