from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

def set_connection():
    try:
        engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
        connection = engine.connect()
        return connection
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        return error


def show_records(connection):
    query = "SELECT * FROM users;"

    try:
        result = connection.execute(text(query))
        return result
    
    except SQLAlchemyError as e:
        print("error", err.__cause__)

    return result



@app.route('/users', methods = ['GET', 'POST'])
def users():
    connection = set_connection()

    if request.method == 'GET':
        records = show_records(connection)
        data = []
        for row in records:
            row_data = {}
            row_data['id'] = row['id']
            row_data['name'] = row['name']
            row_data['email'] = row['email']
            data.append(row_data)

    connection.close()
    return jsonify(data)

@app.route('/')
def home():
    return jsonify({"message": "Hello, Docker!"})



if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True)  # Enable debug mode