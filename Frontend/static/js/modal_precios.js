document.addEventListener("DOMContentLoaded", function() {
    var editButtons = document.querySelectorAll(".edit-button");
    var modal = document.getElementById("modal");
    var closeModalButton = document.getElementById("closeModal");
    var precioForm = document.getElementById("precioForm");
    var precioNocheInput = document.getElementById("precioNoche");
    var errorMessage = document.getElementById("error-message");

    editButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var id = button.getAttribute("data-id");
            var precio = button.getAttribute("data-precio");
            document.getElementById("habitacionId").value = id;
            precioNocheInput.value = precio;
            modal.style.display = "block";
        });
    });

    closeModalButton.addEventListener("click", function() {
        modal.style.display = "none";
    });

    precioForm.addEventListener("submit", function(event) {
        var nuevoPrecio = precioNocheInput.value;
        if (!(/^\d*\.?\d+$/.test(nuevoPrecio))) {
            event.preventDefault();
            errorMessage.style.display = "block";
        } else {
            errorMessage.style.display = "none";
        }
    });
});
