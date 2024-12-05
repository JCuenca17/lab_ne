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
