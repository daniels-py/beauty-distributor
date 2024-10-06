document.addEventListener('DOMContentLoaded', () => {
    ListarCategorias();
});

function ListarCategorias() {
    fetch("http://127.0.0.1:8000/categorias/", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(datos => {
        let tabla = document.querySelector('#tabla-categorias-body');
        tabla.innerHTML = "";

        if (!datos.categorias || datos.categorias.length === 0) {
            tabla.innerHTML += `<tr><td colspan="4">No existen datos registrados</td></tr>`;
        } else {
            datos.categorias.forEach(categoria => {
                tabla.innerHTML += `
                <tr>
                    <td>${categoria.id}</td>
                    <td>${categoria.nombre}</td>
                    <td>${categoria.descripcion}</td>
                    <td>${categoria.permite_color}</td> <!-- Asegúrate de mostrar el campo permite_color -->
                    <td>
                    <div class="btn-container">
                        <button class="btnEliminar" onclick="EliminarCategoria(${categoria.id})">Eliminar</button>
                    </div>
                    </td>
                </tr>`;
            });
        }
    })
    .catch(error => {
        console.error('Error al obtener las categorías:', error);
    });
}
