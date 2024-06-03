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

@app.route('/')
def home():
    return jsonify({"message": "Hello, Docker!"})

if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 