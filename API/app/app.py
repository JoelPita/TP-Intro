from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')

# ------- Endpoints para Reviews -----------
# ---Crear Review ---
@app.route('/reviews', methods=['POST'] ) 
def create_review():
    new_review= request.get_json()
    # --- Me aseguro que la request venga con name y text ----
    if not new_review or 'name' not in new_review or 'text' not in new_review:
        return jsonify({'message': "Datos incompletos"}), 400
    query = text("INSERT INTO Reviews (nombre_autor, texto) VALUES (:nombre_autor, :texto)")
    try:
        with engine.connect() as conn: # <--------------------Cuando se arme la funcion final reemplazar AQUI.
            conn.execute(query, {'nombre_autor': new_review['name'], 'texto':new_review['text']})
            conn.commit()
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    return jsonify({'message': "Se ha agregado correctamente"}), 201

# ---Actualizar el estado de visibilidad ---
@app.route('/reviews/<int:id>/visibility', methods=['PUT'] ) 
def update_visibility(id):
    new_status= request.get_json().get('visible')
    # --- Me aseguro que la request venga con un status----
    if new_status is None:
        return jsonify({'message': "Datos incompletos"}), 400
    query = text("UPDATE Reviews SET visible = :visible WHERE id= :id")
    try:
        with engine.connect() as conn: # <--------------------Cuando se arme la funcion final reemplazar AQUI.
            result = conn.execute(query, {'visible': new_status, 'id': id})
            conn.commit()
            # --- Verifica si existe una review para el id ----
            if  result.rowcount == 0:
                return jsonify({'message': 'Review no encontrada para el id especificado'}), 404
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    return jsonify({'message': "Se ha modificado la visibilidad correctamente"}), 200


# --- Obtener todas las reviews (para el administrador) ---
@app.route('/reviews', methods=['GET'])
def get_all_reviews():
    query = text("SELECT * FROM Reviews")
    try:
        with engine.connect() as conn: # <--------------------Cuando se arme la funcion final reemplazar AQUI.
            result = conn.execute(query)
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    reviews = []
    for row in result:
        entity = {}
        entity['id'] = row.id
        entity['nombre_autor'] = row.nombre_autor
        entity['texto'] = row.texto
        entity['visible'] = row.visible
        entity['estado']= row.estado
        reviews.append(entity)

    return jsonify(reviews), 200

# --- Obtener todas las reviews con visibilidad confirmada (para el main) ---
@app.route('/reviews/visible', methods=['GET'])
def get_visible_reviews():
    query = text("SELECT * FROM Reviews WHERE visible = true")
    try:
        with engine.connect() as conn:
            result = conn.execute(query)
    except SQLAlchemyError as err:
        error_message = str(err.__cause__) if err.__cause__ else str(err)
        return jsonify({'message': "Se ha producido un error: " + error_message}), 500
    
    reviews = []
    for row in result:
        entity = {}
        entity['id'] = row.id
        entity['nombre_autor'] = row.nombre_autor
        entity['texto'] = row.texto
        entity['visible'] = row.visible
        entity['estado']= row.estado
        reviews.append(entity)

    return jsonify(reviews), 200    
    
@app.route('/reservas', methods=['POST'])
def create_reserva():
    data = request.json
    query = text("""
        INSERT INTO Reservas (email_cliente, nombre_cliente, telefono_cliente, fecha_desde, fecha_hasta, 
            cantidad_habitaciones, cantidad_personas, metodo_pago, estado, precio_total, habitacion_id) 
        VALUES (:email_cliente, :nombre_cliente, :telefono_cliente, :fecha_desde, :fecha_hasta, :cantidad_habitaciones, 
            :cantidad_personas, :metodo_pago, :estado, :precio_total, :habitacion_id)
        """)
    
    try:
        conn = engine.connect()
        conn.execute(query, {
            'email_cliente': data['email_cliente'],
            'nombre_cliente': data['nombre_cliente'],
            'telefono_cliente': data['telefono_cliente'],
            'fecha_desde': data['fecha_desde'],
            'fecha_hasta': data['fecha_hasta'],
            'cantidad_habitaciones': data['cantidad_habitaciones'],
            'cantidad_personas': data['cantidad_personas'],
            'metodo_pago': data['metodo_pago'],
            'estado': "pendiente",
            'precio_total': data['precio_total'],
            'habitacion_id': data['habitacion_id']
        })
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Reserva añadida correctamente"}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"message": error}), 500
    
@app.route('/reservas', methods=['GET'])
def get_reservas():
    estado = request.args.get('estado')
    if estado:
        query = text("SELECT * FROM Reservas WHERE estado = :estado")
        params = {'estado': estado}
    else:
        query = text("SELECT * FROM Reservas")
        params = {}

    try:
        conn = engine.connect()
        result = conn.execute(query, params)
        reservas = []
        for row in result:
            reserva = {
                'id': row[0],
                'email_cliente': row[1],
                'nombre_cliente': row[2],
                'telefono_cliente': row[3],
                'fecha_desde': row[4],
                'fecha_hasta': row[5],
                'cantidad_habitaciones': row[6],
                'cantidad_personas': row[7],
                'metodo_pago': row[8],
                'estado': row[9],
                'motivo_rechazo': row[10],
                'precio_total': row[11],
                'habitacion_id': row[12]
            }
            reservas.append(reserva)
        conn.close()
        return jsonify({"success": True, "reservas": reservas}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500
    


@app.route('/reservas/<int:id>/confirm', methods=['PUT'])
def confirm_reserva(id):
    data = request.json
    estado = data['estado']
    
    if estado not in ['aceptada', 'rechazada']:
        return jsonify({"success": False, "message": "Estado inválido. Solo se permite 'aceptada' o 'rechazada'."}), 400
    
    motivo_rechazo = data['motivo_rechazo']
    query = text("""
        UPDATE Reservas 
        SET estado = :estado, motivo_rechazo = :motivo_rechazo
        WHERE id = :id
        """)
        
    try:
        conn = engine.connect()
        conn.execute(query, {
            'estado': estado,
            'motivo_rechazo': motivo_rechazo,
            'id': id
        })
        conn.commit()
        conn.close()
        
        #TO DO: IMPLEMENTAR ENVIO DE MAIL
        send_email(data['email_cliente'], estado, motivo_rechazo)

        return jsonify({"success": True, "message": "Reserva actualizada correctamente"}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500

def send_email(email, estado, motivo_rechazo):
    pass



@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    query = text("DELETE FROM Users WHERE id = :id")
    validation_query = text("SELECT * FROM Users WHERE id = :id")
    try:
        conn = engine.connect()
        val_result = conn.execute(validation_query, {'id': id})
        if val_result.rowcount == 0:
            conn.close()
            return jsonify({"message": "Usuario no encontrado"}), 404
        conn.execute(query, {'id': id})
        conn.commit()
        conn.close()
        return jsonify({"message": "Usuario eliminado correctamente"}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return jsonify({"message": error}) , 500

@app.route('/')
def home():
    return jsonify({"message": "Hello, Docker!"})

if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 