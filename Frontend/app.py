from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/servicios.html')
def servicios():
    return render_template('servicios.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 