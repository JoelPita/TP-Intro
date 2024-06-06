from flask import Flask, request, url_for, jsonify, render_template, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 