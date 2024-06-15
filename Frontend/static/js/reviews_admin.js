document.addEventListener('DOMContentLoaded', function () {
    // El contenedor de la lista y los elementos
    const reviewsList = document.getElementById('reviews-list');
    const searchInput = document.getElementById('search-input');
    let reviewsElements = Array.from(document.querySelectorAll('.review-item'));
    // Elementos de la paginacion
    const itemsPerPage = 5;
    let currentPage = 1;
    let filteredReviews = reviewsElements;

    // Funcion que agrega los eventos y debe usarse una sola vez
    function addEventListeners() {
        reviewsElements.forEach(reviewElement => {
            const id = reviewElement.getAttribute('data-id');
            const visibilityButton = reviewElement.querySelector('.visibility-button');
            const estadoButton = reviewElement.querySelector('.estado-button');
            
            // Evento de visibilidad
            visibilityButton.addEventListener('click', function () {
                if (this.disabled) return;
                this.disabled = true; // controlo que no se hagan varios clicks seguidos
                const visible = reviewElement.getAttribute('data-visible') === 'true';
                updateVisibility(id, visible, this, reviewElement);
            });

            estadoButton.addEventListener('click', function () {
                if (this.disabled) return;
                this.disabled = true; // controlo que no se hagan varios clicks seguidos
                const estado = reviewElement.getAttribute('data-estado');
                updateEstado(id, estado, this, reviewElement);
            });
        });
    }

    // Eventos en botones
    function updateVisibility(id, visible, button, reviewElement) {
        fetch(`http://localhost:5000/reviews/${id}/visibility`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ visible: !visible })
        })
        .then(response => response.json())
        .then(data => {
            alert("Perfecto. " + data.message);
            reviewElement.setAttribute('data-visible', !visible);
            updateVisibleButton(button, !visible); // Actualizo el contenido del boton
            button.disabled = false; // Reactivo el boton
        })
        .catch(error => {
            alert('Error al actualizar la visibilidad');
            button.disabled = false;
        });
    }

    function updateEstado(id, estado, button, reviewElement) {
        const newEstado = (estado === 'nueva' || estado === 'favorita') ? 'desmarcada' : 'favorita';
        fetch(`http://localhost:5000/reviews/${id}/state`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: newEstado })
        })
        .then(response => response.json())
        .then(data => {
            alert("Estado actualizado: " + data.message);
            reviewElement.setAttribute('data-estado', newEstado);
            button.textContent = newEstado === 'desmarcada' ? 'Marcar como favorita' : 'Quitar de favorita';
            button.disabled = false; 
        })
        .catch(error => {
            alert('Error al actualizar el estado');
            button.disabled = false; 
        });
    }

    // Cambio visual de los botones al tocarlos.
    function updateVisibleButton(button, newVisible) {
        button.textContent = newVisible ? 'Ocultar' : 'Mostrar';
        button.className = newVisible ? 'btn btn-danger visibility-button' : 'btn btn-success visibility-button';
    }

    // Renderiza la vista cada vez que se toca un boton de cambio de estado o de siguiente pagina.
    function renderReviews() {
        reviewsList.innerHTML = ''; // Limpiar la lista de reviews
        let start = (currentPage - 1) * itemsPerPage;
        let end = start + itemsPerPage;
        filteredReviews.slice(start, end).forEach(review => {
            reviewsList.appendChild(review);
        });
        updatePagination();
    }

    // Agrego eventos al tocar un boton de filtro por estado de reviews
    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', function () {
            const criterio = this.getAttribute('data-filtro')
            const filter = this.getAttribute(criterio);
            filteredReviews = reviewsElements.filter(review => filter === 'all' || review.getAttribute(criterio) === filter);
            currentPage = 1;
            renderReviews();
        });
    });

    // Función de búsqueda
    function searchReviews(query) {
        query = query.toLowerCase();
        filteredReviews = reviewsElements.filter(review => {
            const text = review.querySelector('.review-text').textContent.toLowerCase();
            const author = review.querySelector('.blockquote-footer').textContent.toLowerCase();
            return text.includes(query) || author.includes(query);
        });
        currentPage = 1; // Resetear a la primera página después de buscar
        renderReviews();
    }

    // Event listener para el campo de búsqueda
    searchInput.addEventListener('input', function () {
        searchReviews(this.value);
    });

    // Función para cambiar de página
    function changePage(newPage) {
        if (newPage < 1 || newPage > Math.ceil(filteredReviews.length / itemsPerPage)) return;
        currentPage = newPage;
        renderReviews();
    }

    // Event listeners para la paginación
    document.getElementById('prev-page').addEventListener('click', function (e) {
        e.preventDefault();
        changePage(currentPage - 1);
    });

    document.getElementById('next-page').addEventListener('click', function (e) {
        e.preventDefault();
        changePage(currentPage + 1);
    });

    // Función para actualizar los botones de paginación
    function updatePagination() {
        const totalPages = Math.ceil(filteredReviews.length / itemsPerPage);
        document.querySelector('#prev-page').parentElement.classList.toggle('disabled', currentPage === 1);
        document.querySelector('#next-page').parentElement.classList.toggle('disabled', currentPage === totalPages);
    }

    // Inicializaciones
    addEventListeners();
    renderReviews();
});
