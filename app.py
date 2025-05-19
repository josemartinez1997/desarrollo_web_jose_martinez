from flask import Flask, request, render_template, redirect, url_for, session, flash
from validations import validar_actividad
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os
from db.db import get_all_actividades, crear_actividad, crear_tema, crear_comuna, crear_contactar_por, crear_foto, crear_region, get_activity


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/")
def index():
    actividades = get_all_actividades()
    actividades = sorted(actividades, key=lambda a: a.dia_hora_inicio, reverse=True)[:5]
    return render_template("templates/index.html", actividades=actividades)

@app.route("/agregar_actividad", methods=["GET", "POST"])
def agregar_Actividad():
    if request.method == "POST":
        datos = request.form
        imagenes = request.files.getlist('fotos')
        errores = validar_actividad(datos, imagenes)
        if errores:
            for error in errores:
                flash(error)
            return render_template("agregar_actividad.html")


        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector', '')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        inicio = request.form.get('inicio')
        termino = request.form.get('termino')
        descripcion = request.form.get('descripcion', '')
        temas = request.form.getlist('tema')
        tema_otro = request.form.get('otro')
        contactos = request.form.getlist('contacto')
        archivos = request.files.getlist('fotos')

        crear_actividad(comuna_id, sector, nombre, email, celular, inicio, termino, descripcion, temas, tema_otro, contactos, archivos)

        actividad = get_activity(comuna_id, sector, nombre, inicio)

        for t in temas:
            if t == tema_otro:
                crear_tema(tema="otro", glosa_otro=tema_otro, actividad_id=actividad.id)
            else:
                crear_tema(tema=t, glosa_otro=None, actividad_id=actividad.id)

if __name__ == "__main__":
    app.run(debug=True)



    
