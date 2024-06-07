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

@app.route('/')
def home():
    return jsonify({"message": "Hello, Docker!"})

if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 