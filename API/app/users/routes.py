from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# ---Crer Blueprint para users ---
users_bp = Blueprint('users', __name__)

# ---Crer rutas para users ---
@users_bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    query = text("DELETE FROM Users WHERE id = :id")
    validation_query = text("SELECT * FROM Users WHERE id = :id")
    try:
        engine = current_app.config['engine']
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
