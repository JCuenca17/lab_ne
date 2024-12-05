document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".clickable-row");

    rows.forEach(row => {
        row.addEventListener("click", function (event) {
            // Evitar que el click en un botón o enlace dentro de la fila haga algo diferente
            if (!event.target.closest("a, button")) {
                const url = this.getAttribute("data-url");
                if (url) {
                    window.location.href = url;
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const openFiltersBtn = document.getElementById('openFiltersBtn');
    const closeFiltersBtn = document.getElementById('closeFiltersBtn');
    const filtersPanel = document.getElementById('filtersPanel');

    // Asegurarse de que los elementos existen antes de intentar usarlos
    if (openFiltersBtn && filtersPanel) {
        openFiltersBtn.addEventListener('click', function () {
            filtersPanel.classList.add('open');
        });
    }

    if (closeFiltersBtn && filtersPanel) {
        closeFiltersBtn.addEventListener('click', function () {
            filtersPanel.classList.remove('open');
        });
    }
});
