from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')

# def set_connection():
#     try:
#         engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
#         connection = engine.connect()
#         return connection
#     except SQLAlchemyError as e:
#         error = str(e.__cause__)
#         return error
    
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
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/habitaciones/<id>', methods = ['GET'])
def habitaciones_id(id):
    return


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 