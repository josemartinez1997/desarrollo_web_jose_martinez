from flask import Flask, request, render_template, redirect, url_for, session
from validations import validate_email
from werkzeug.utils import secure_filename
import hashlib
import filetype
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)

app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/agregar_actividad", methods=["GET", "POST"])
def agregar_Actividad():
    
