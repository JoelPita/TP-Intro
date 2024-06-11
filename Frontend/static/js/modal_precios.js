modal_precios.js

document.addEventListener("DOMContentLoaded", function() {
    var editButtons = document.querySelectorAll(".edit-button");
    var modal = document.getElementById("editModal");
    var precioForm = document.getElementById("editForm");
    var precioNocheInput = document.getElementById("precio");
    var errorMessage = document.getElementById("error-message");
   ;
    
    editButtons.forEach(function(button) {
        button.addEventListener("click", function() {
        var id = button.getAttribute("data-id");
        var precio = button.getAttribute("data-precio");
        document.getElementById("habitacionId").value = id;
        precioNocheInput.value = precio;
        modal.style.display = "block";
        errorMessage.style.display = "none"; // Oculta el mensaje de error al abrir el modal
        });
    });

    precioForm.addEventListener("submit", function(event) {
    // Evita el comportamiento predeterminado del envío del formulario
    event.preventDefault();
            
    var nuevoPrecio = precioNocheInput.value;
    if (!(/^\d*\.?\d+$/.test(nuevoPrecio))) {
        errorMessage.style.display = "block";
    } else {
        errorMessage.style.display = "none";
            // Envía el formulario si la validación es exitosa
            precioForm.submit();
        }
    });
 });