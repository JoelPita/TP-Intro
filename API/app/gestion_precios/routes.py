from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# ---Crear Blueprint para gestion de precios ---
gestion_precios_bp = Blueprint('gestion_precios', __name__)

# Esta funcion pertenece al modulo de habitaciones. 
# La creé acá para que mi módulo funcione hasta que la verdadera sea agregada al proyecto. 
@gestion_precios_bp.route('/obtener-habitaciones', methods=['GET']) 
def obtener_habitaciones():
    query = text("SELECT * FROM Habitaciones")
    try:
        engine = current_app.config['engine']
        connection = engine.connect()
        result = connection.execute(query)
        connection.close()  
        if result.rowcount != 0:
            data = []
            for row in result:
                entity = {
                    'id': row.id,
                    'nombre': row.nombre,
                    'descripcion': row.descripcion,
                    'precio_noche': str(row.precio_noche)
                }
                data.append(entity)
            return jsonify(data), 200
        return jsonify({"message": "No existen habitaciones"}), 404
    except SQLAlchemyError as err:
        error = str(err.__cause__)
        return jsonify({"message": error}), 500

@gestion_precios_bp.route('/gestion_precios', methods=['PATCH'])
def actualizar_precios_habitaciones():
    datos = request.get_json()
    nuevo_precio = datos.get('precio_noche')
    id_habitacion = datos.get('id')    
    
    query = text("UPDATE Habitaciones SET precio_noche = :precio_noche WHERE id = :id")        
    try:          
        connection = current_app.config['engine'].connect()
        result = connection.execute(query, {'precio_noche': nuevo_precio, 'id': id_habitacion})
        if result.rowcount == 0:
            connection.close()
            return jsonify({'message': 'Habitación no encontrada'}), 404 
        else:
            connection.commit()
            connection.close()
            return jsonify({'message': 'Precio actualizado correctamente'}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return jsonify({'message': error}), 500