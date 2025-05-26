# 🧾 1. Ver todas las comandas

@app.route('/comandes')
def llistarComandes():
    dades = vols().llistaComandes()  # esta función la defines tú
    return render_template('comandes.html', comandes=dades)

# 🍽 2. Consultar una comanda concreta y sus plats

@app.route('/comanda/<int:id_comanda>')
def veureComanda(id_comanda):
    plats = vols().platsDeComanda(id_comanda)
    return render_template('comanda.html', plats=plats, id_comanda=id_comanda)

# ➕ 3. Afegir una comanda nova (GET per mostrar el formulari, POST per afegir)

@app.route('/afegir_comanda', methods=['GET', 'POST'])
def afegirComanda():
    if request.method == 'POST':
        taula = request.form['taula']
        estat = request.form['estat']
        preu = request.form['preu']
        vols().insertaComanda(taula, estat, preu)
        return redirect(url_for('llistarComandes'))
    return render_template('afegir_comanda.html')

# HTML (simplificat):

<form method="post">
    Taula: <input type="number" name="taula">
    Estat: <select name="estat">
        <option value="comanat">Comanat</option>
        <option value="preparat">Preparat</option>
        ...
    </select>
    Preu: <input type="number" step="0.01" name="preu">
    <button type="submit">Crear comanda</button>
</form>

# 🍝 4. Afegir plats a una comanda concreta

@app.route('/afegir_plats/<int:id_comanda>', methods=['GET', 'POST'])
def afegirPlatsAComanda(id_comanda):
    if request.method == 'POST':
        id_plat = request.form['id_plat']
        quantitat = request.form['quantitat']
        vols().afegirPlatAComanda(id_comanda, id_plat, quantitat)
        return redirect(url_for('veureComanda', id_comanda=id_comanda))
    plats = vols().llistaPlats()
    return render_template('afegir_plat.html', plats=plats, id_comanda=id_comanda)

# 🆕 5. Afegir nou plat a la carta

@app.route('/afegir_plat', methods=['GET', 'POST'])
def afegirPlat():
    if request.method == 'POST':
        tipus = request.form['tipus']
        nom = request.form['nom']
        vols().insertaPlat(tipus, nom)
        return redirect(url_for('llistaPlats'))
    return render_template('afegir_plat.html')

# 6. Añadir columna tasas

def agregar_campo_tasas(self):
    """
    Añade el campo 'tasas' a la tabla airports con valores por defecto:
    - 40 para España
    - 30 para Portugal
    - 50 para otros países
    """
    self.conecta()

    # 1. Añadir la columna si no existe
    sql_alter = "ALTER TABLE airports ADD COLUMN tasas DECIMAL(10,2) DEFAULT 50"
    self.cursor.execute(sql_alter)

    # 2. Actualizar registros según país
    sql_update_es = "UPDATE airports SET tasas = 40 WHERE country = 'ESPAÑA'"
    sql_update_pt = "UPDATE airports SET tasas = 30 WHERE country = 'PORTUGAL'"

    self.cursor.execute(sql_update_es)
    self.cursor.execute(sql_update_pt)

    self.desconecta()


# 7. Calcular total de una comanda

@app.route('/calcula_total/<int:id_comanda>')
def calculaTotal(id_comanda):
    vols().actualitzaPreuComanda(id_comanda)
    return redirect(url_for('veureComanda', id_comanda=id_comanda))

# 8. Actualizar el estado de una comanda

@app.route('/canviar_estat/<int:id_comanda>', methods=['POST'])
def canviarEstat(id_comanda):
    nou_estat = request.form['estat']
    vols().actualitzaEstat(id_comanda, nou_estat)
    return redirect(url_for('veureComanda', id_comanda=id_comanda))

# Ejemplo de html

<form method="post" action="{{ url_for('canviarEstat', id_comanda=comanda.id_comanda) }}">
  <select name="estat">
    <option value="comanat">Comanat</option>
    <option value="preparat">Preparat</option>
    <option value="cobrat">Cobrat</option>
    <option value="finalitzat">Finalitzat</option>
  </select>
  <button type="submit">Actualitzar estat</button>
</form>

#  Mostrar alertas y validaciones

from flask import flash

@app.route('/afegir_plat/<int:id_comanda>', methods=['POST'])
def afegirPlat(id_comanda):
    if not vols().comandaExisteix(id_comanda):
        flash("Error: la comanda no existeix.")
        return redirect(url_for('llistarComandes'))
    # resto del codi

{% with messages = get_flashed_messages() %}
  {% if messages %}
    <ul>
      {% for msg in messages %}
        <li>{{ msg }}</li>
      {% endfor %}
    </ul>
  {% endif %}
{% endwith %}

# 9. Mostrar los platos de una comanda específica

@app.route('/canviar_estat/<int:id_comanda>', methods=['POST'])
def canviarEstat(id_comanda):
    nou_estat = request.form['estat']
    vols().actualitzaEstat(id_comanda, nou_estat)
    return redirect(url_for('veureComanda', id_comanda=id_comanda))



<h1 class="text-3xl font-bold mb-6 text-center">Fer comanda</h1>
{% if missatge %}
  <div class="mb-4 p-4 rounded text-white font-semibold {% if color == 'green' %}bg-green-500{% else %}bg-red-500{% endif %}">
    {{ missatge }}
  </div>
{% endif %}

<div class="max-w-md mx-auto bg-white p-6 rounded shadow mb-8">
  <form method="get" action="{{ url_for('verifica') }}">
    <div class="mb-4">
      <label class="block font-bold mb-1">Número de taula</label>
      <input type="number" name="taula" value="1"
        class="w-full px-3 py-2 border border-gray-300 rounded">
    </div>



@app.route('/verifica')
def verifica():
    taula = int(request.args.get('taula'))
    comensals = int(request.args.get('comensals'))

    # Aquí criden la funció que hauran de completar
    missatge, color = analitzaComanda(taula, comensals)

    plats = restaurant().carregaPlats()
    return render_template('index.html', plats=plats, missatge=missatge, color=color)


# Aquesta és la funció que hauran de completar
def analitzaComanda(taula, comensals):
    if comensals <= 0:
        return "El número de comensals ha de ser més gran que 0", "red"
    if not restaurant().taulaBuida(taula):
        return "La taula està OCUPADA", "red"











# Exemples fastapi

# ✅ 1. Importaciones y configuración base

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import vols  # tu clase de conexión a BD

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🧾 2. Listar todas las comandas

@app.get("/comandes")
def llistar_comandes(request: Request):
    dades = vols().llistaComandes()
    return templates.TemplateResponse("comandes.html", {"request": request, "comandes": dades})

# 🍽 3. Ver una comanda específica y sus platos

@app.get("/comanda/{id_comanda}")
def veure_comanda(id_comanda: int, request: Request):
    plats = vols().platsDeComanda(id_comanda)
    return templates.TemplateResponse("comanda.html", {"request": request, "plats": plats, "id_comanda": id_comanda})

# ➕ 4. Afegir una comanda nova (GET i POST)

@app.get("/afegir_comanda")
def formulari_comanda(request: Request):
    return templates.TemplateResponse("afegir_comanda.html", {"request": request})

@app.post("/afegir_comanda")
def afegir_comanda(taula: int = Form(...), estat: str = Form(...), preu: float = Form(...)):
    vols().insertaComanda(taula, estat, preu)
    return RedirectResponse(url="/comandes", status_code=303)

# 🍝 5. Afegir plats a una comanda

@app.get("/afegir_plats/{id_comanda}")
def formulari_plats(id_comanda: int, request: Request):
    plats = vols().llistaPlats()
    return templates.TemplateResponse("afegir_plat.html", {"request": request, "plats": plats, "id_comanda": id_comanda})

@app.post("/afegir_plats/{id_comanda}")
def afegir_plat(id_comanda: int, id_plat: int = Form(...), quantitat: int = Form(...)):
    vols().afegirPlatAComanda(id_comanda, id_plat, quantitat)
    return RedirectResponse(url=f"/comanda/{id_comanda}", status_code=303)

# 🆕 6. Afegir nou plat a la carta

@app.get("/afegir_plat")
def formulari_nou_plat(request: Request):
    return templates.TemplateResponse("afegir_plat.html", {"request": request})

@app.post("/afegir_plat")
def afegir_nou_plat(tipus: str = Form(...), nom: str = Form(...)):
    vols().insertaPlat(tipus, nom)
    return RedirectResponse(url="/comandes", status_code=303)