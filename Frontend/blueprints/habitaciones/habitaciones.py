from flask import Blueprint, render_template

habitacionesBp = Blueprint("habitacionesBp", __name__)

@habitacionesBp.route('/', methods=['GET'])
def habitaciones():
    lista_habitaciones = get_habitaciones()
    return render_template('habitaciones.html', habitaciones = lista_habitaciones)

@habitacionesBp.route('/<id>', methods = ['GET'])
def habitaciones_id(id):
    return render_template('habitacion.html', id=id)

def get_habitaciones():
    lista_habitaciones = [{"id": 1, "nombre": "habitacion deluxe", "descripcion": "La habitación es una porqueria."},{"id": 2, "nombre": "habitacion menos deluxe", "descripción": "La habitación es mas porqueria."},{"id": 3, "nombre": "habitacion mucho menos deluxe", "descripción": "La habitación es mucho mas porqueria."}]
    return render_template("habitaciones.html", habitaciones=lista_habitaciones)