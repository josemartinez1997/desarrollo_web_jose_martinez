import re
import filetype
from datetime import datetime

def validar_region(value):
    if int(value) >= 1 or int(value) <= 16:
        return True
    return False

def validar_comuna(value):
    if int(value) >= 10101 or int(value) <= 130606:
        return True
    return False

def validar_email(value):
    emailRedex = r'^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(emailRedex, value)) and 0<len(value) and len(value)<101

def validar_tel(value):
    telRedex = r'^\+569.\d{8}$'
    return bool(re.match(telRedex, value))

def validar_nombre(value):
    if len(value) == 0:
        return True
    if len(value) < 201:
        return False
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-]+$', value):
        return False
    return True
    
def validar_sector(value):
    if len(value) == 0:
        return True
    elif len(value)>100:
        return False
    return True

def validar_contacto(value, texto):
    if value=='6':
        if len(value) < 3 and len(value) > 50:
            return False
        return True
    return True

def validar_tema(value, texto):
    if value=='10':
        if len(value) < 3 and len(value) > 15:
            return False
        return True
    return True

def validar_conf_img(conf_img):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if conf_img is None:
        return False

    # check if the browser submitted an empty file
    if conf_img.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(conf_img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validar_inicio(value):
    try:
        fecha = datetime.strptime(value, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False
def validar_final(fecha_inicio_value, fecha_final_value):
    formato = '%Y-%m-%d %H:%M'
    msg = ''
    fecha_inicio = datetime.strptime(fecha_inicio_value, formato)
    try:
        fecha_final = datetime.strptime(fecha_final_value, formato)
    except ValueError:
        msg=msg+'Fecha final invalida'
        return False, msg
    if fecha_inicio > fecha_final:
        msg = msg + 'La fecha final no puede ser anterior a la fecha inicial'
        return False, msg
    else:
        return True


def validar_actividad(comuna, region, nombre, email, celular, contacto, inicio, termino, tema, foto):
    msg=''
    ff, mensaje_ff = validar_final(inicio, termino)
    if not validar_comuna(comuna):
        msg=msg+'Ingrese comuna'
    if not validar_region(region):
        msg=msg+'Ingrese región'
    if not validar_email(email):
        msg=msg+'Email inválido'
    if not validar_tel(celular):
        msg=msg+'Formato inválido'
    if not validar_nombre(nombre):
        msg=msg+' Nombre demasiado largo'
    if not validar_contacto(contacto):
        msg=msg+'Formato inválido'
    if not ff:
        msg=msg+mensaje_ff
    if not validar_contacto(contacto):
        msg=msg+'Ingrese contacto válido'
    if not validar_tema(tema):
        msg=msg+'Ingrese tema válido'
    if msg=='':
        return True, msg
    else:
        return False, msg

def validate_fotos(foto):
    if validar_conf_img(foto):
        return True
    return False


