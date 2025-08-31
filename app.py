from flask import Flask, render_template_string, request, send_file
from docx import Document
from io import BytesIO

app = Flask(__name__)

FORM_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Generar Cotización</title>
<style>
    body { font-family: Arial, sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
    .container { max-width: 900px; margin: 20px auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); }
    h2, h3 { text-align: center; color: #333; }
    form { display: flex; flex-direction: column; gap: 15px; }
    label { font-weight: bold; margin-bottom: 5px; display: block; }
    input[type="text"], input[type="number"], input[type="date"], select {
        padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%; box-sizing: border-box;
    }
    button {
        padding: 14px; border: none; border-radius: 8px;
        background-color: #007bff; color: #fff; font-size: 16px;
        cursor: pointer; transition: background 0.3s; width: 100%;
    }
    button:hover { background-color: #0056b3; }
    .concepto-item {
        display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;
    }
    .concepto-item input, .concepto-item select { flex: 1; min-width: 120px; }
    .concepto-item button { flex: 0.5; background-color: #dc3545; }
    .concepto-item button:hover { background-color: #a71d2a; }
    #conceptos-container { margin-bottom: 10px; }
    .add-btn { margin-bottom: 15px; background-color: #28a745; }
    .add-btn:hover { background-color: #1c7c31; }
    .totales { font-weight: bold; text-align: right; margin-top: 10px; }

    /* 📱 Responsividad en pantallas chicas */
    @media (max-width: 600px) {
        .container { padding: 15px; margin: 10px; }
        .concepto-item { flex-direction: column; }
        .concepto-item input, .concepto-item select, .concepto-item button { width: 100%; }
        .totales { text-align: left; }
    }
</style>
<script>
function agregarConcepto() {
    const container = document.getElementById("conceptos-container");
    const div = document.createElement("div");
    div.className = "concepto-item";
    div.innerHTML = `
        <input type="text" name="concepto[]" placeholder="Concepto" required>
        <input type="number" name="cantidad[]" placeholder="Cantidad" min="0" step="0.01" required oninput="calcularTotales()">
        <select name="unidad[]">
            <option value="Pza">Pza</option>
            <option value="Kg">Kg</option>
            <option value="m">m</option>
            <option value="L">L</option>
        </select>
        <input type="number" name="valor_unitario[]" placeholder="Valor Unitario" min="0" step="0.01" required oninput="calcularTotales()">
        <input type="text" class="subtotal" placeholder="Subtotal" readonly>
        <button type="button" onclick="this.parentElement.remove(); calcularTotales()">Eliminar</button>
    `;
    container.appendChild(div);
    calcularTotales();
}

function calcularTotales() {
    let totalMateriales = 0;
    const items = document.querySelectorAll(".concepto-item");
    items.forEach(item => {
        const cantidad = parseFloat(item.querySelector('input[name="cantidad[]"]').value) || 0;
        const valor = parseFloat(item.querySelector('input[name="valor_unitario[]"]').value) || 0;
        const subtotal = cantidad * valor;
        item.querySelector('.subtotal').value = `$${subtotal.toFixed(2)} MXN`;
        totalMateriales += subtotal;
    });
    const manoObra = parseFloat(document.getElementById("mano_obra").value) || 0;
    const gestion = parseFloat(document.getElementById("gestion").value) || 0;
    const totalGeneral = totalMateriales + manoObra + gestion;
    document.getElementById("total_materiales").innerText = `$${totalMateriales.toFixed(2)} MXN`;
    document.getElementById("total_general").innerText = `$${totalGeneral.toFixed(2)} MXN`;
}

window.onload = function() {
    agregarConcepto(); // agrega un concepto inicial
    document.getElementById("mano_obra").oninput = calcularTotales;
    document.getElementById("gestion").oninput = calcularTotales;
};
</script>
</head>
<body>
<div class="container">
    <h2>Generar Cotización</h2>
    <form method="POST" action="/generar">
        <label>Fecha:</label>
        <input name="fecha" type="date" required>

        <label>Nombre del cliente:</label>
        <input name="nombre_cliente" type="text" placeholder="Ej: Juan Pérez" required>

        <label>Título de cotización:</label>
        <input name="titulo_cotizacion" type="text" placeholder="Ej: Instalación de calentadores">

        <label>Plazo de la oferta:</label>
        <input name="plazo_oferta" type="text" placeholder="Ej: 15 días">

        <label>Tiempo de entrega:</label>
        <input name="tiempo_entrega" type="text" placeholder="Ej: 7 días hábiles">

        <label>Pago acordado:</label>
        <input name="pago_acordado" type="text" placeholder="Ej: 50% anticipo">

        <h3>Conceptos</h3>
        <div id="conceptos-container"></div>
        <button type="button" class="add-btn" onclick="agregarConcepto()">Agregar concepto</button>

        <label>Mano de obra:</label>
        <input name="mano_obra" id="mano_obra" type="number" value="500" min="0" step="0.01">

        <label>Gestión:</label>
        <input name="gestion" id="gestion" type="number" value="100" min="0" step="0.01">

        <div class="totales">
            Total materiales: <span id="total_materiales">$0.00 MXN</span><br>
            Total general: <span id="total_general">$0.00 MXN</span>
        </div>

        <button type="submit">Generar Word</button>
    </form>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(FORM_HTML)

@app.route("/generar", methods=["POST"])
def generar():
    # Aquí va tu lógica de generación de Word (no lo modifiqué)
    return "Generar DOCX..."

if __name__ == "__main__":
    app.run(debug=True)

