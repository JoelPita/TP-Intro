document.addEventListener("DOMContentLoaded", () => {

    let apiBaseUrl = 'http://127.0.0.1:5000';
    const form = document.getElementById("form_reserva");
    const mensajesError = document.getElementById("mensajes_error");
    const precioTotalElement = document.getElementById("precio_total");

    const campoFechaDesde = document.querySelector('input[name="fecha_desde"]');
    const campoFechaHasta = document.querySelector('input[name="fecha_hasta"]');
    const campoHabitacionId = document.querySelector('select[name="habitacion_id"]');
    const campoCantidadHabitaciones = document.querySelector('input[name="cantidad_habitaciones"]');

    // Añadir event listeners a los campos específicos
    [campoFechaDesde, campoFechaHasta, campoHabitacionId, campoCantidadHabitaciones].forEach(campo => {
        campo.addEventListener('input', actualizarPrecioTotal);
    });

    function actualizarPrecioTotal() {
        console.log('Actualizando precio total');
        const fechaDesde = campoFechaDesde.value;
        const fechaHasta = campoFechaHasta.value;
        const habitacionId = campoHabitacionId.value;
        const cantidadHabitaciones = campoCantidadHabitaciones.value;

        if (fechaDesde && fechaHasta && fechaDesde.length === 10 && fechaHasta.length === 10 && habitacionId && cantidadHabitaciones) {
            // Calcular cantidad de noches
            const cantidadNoches = Math.round((new Date(fechaHasta) - new Date(fechaDesde)) / (1000 * 3600 * 24));

            if (!cantidadNoches > 0) {
                mostrarErrores(['La estadia debe ser de al menos una noche']);
                return;
            }

            const urlConsultaPrecio = new URL(`${apiBaseUrl}/reservas/calcular-precio`);
            urlConsultaPrecio.searchParams.append('habitacionId', habitacionId);
            urlConsultaPrecio.searchParams.append('cantidadHabitaciones', cantidadHabitaciones);
            urlConsultaPrecio.searchParams.append('cantidadNoches', cantidadNoches);

            // Realizar la consulta del precio total
            fetch(urlConsultaPrecio, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.precioTotal) {
                    precioTotalElement.textContent = `Total: $${data.precioTotal}`;
                } else {
                    mostrarErrores([data.error || 'Error al calcular el precio']);
                }
            })
            .catch(error => {
                mostrarErrores(['Error de red al calcular el precio']);
            });
        }
    }

    form.addEventListener("submit", function(event) {
        mensajesError.innerHTML = ""; // Clear previous errors
        const email = document.querySelector('input[name="email_cliente"]').value;
        const fechaDesde = campoFechaDesde.value;
        const fechaHasta = campoFechaHasta.value;

        let errores = [];

        // Validación de fechas
        if (new Date(fechaHasta) < new Date(fechaDesde)) {
            errores.push("La fecha 'Hasta' no puede ser anterior a la fecha 'Desde'.");
        }

        // Validación de email
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(email)) {
            errores.push("El email no tiene un formato válido.");
        }

        // Si hay errores, prevenir el envío del formulario
        if (errores.length > 0) {
            event.preventDefault();
            mostrarErrores(errores);
            return;
        }
    });

    function mostrarErrores(errores) {
        mensajesError.innerHTML = ""; // Clear previous errors
        errores.forEach(error => {
            const errorItem = document.createElement("p");
            errorItem.textContent = error;
            mensajesError.appendChild(errorItem);
        });
    }
});