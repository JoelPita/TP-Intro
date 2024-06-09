from flask import Flask, request, render_template, url_for, redirect
import requests

app = Flask(__name__)
    
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

@app.route('/actualizar_precios', methods = ['GET'])
def modificar_precios_habitaciones():
    obtener_habitaciones = 'http://127.0.0.1:5000/gestion_precios/obtener-habitaciones' #se reemplazara por el endpoint correspondiente cuando esté disponible
                    #no logro que funcione con url_for('gestion_precios.obtener_habitaciones', _external=True)
    try:                       
        response = requests.get(obtener_habitaciones)
        if response.status_code == 200:
            datos = response.json()
            return render_template('gestion_precios.html', datos=datos)
        elif response.status_code == 404:
            return render_template('404.html')
        else:
            return render_template('404.html')  #deberia ser pagina de error 500
    except requests.RequestException:
        return render_template('404.html')      #deberia ser pagina de error 500
    
@app.route('/actualizar_precios', methods=['POST'])
def enviar_precios_habitaciones():
    id_habitacion = request.form['id']
    nuevo_precio = str(request.form['precio_noche'])
    actualizar_precio = 'http://127.0.0.1:5000/gestion_precios/gestion_precios'
                     #no logro que funcione con url_for('gestion_precios.actualizar_precios_habitaciones', _external=True)
    try:
        response = requests.patch(actualizar_precio, json={'id': id_habitacion, 'precio_noche': nuevo_precio})

        if response.status_code == 200:
            return redirect(url_for('modificar_precios_habitaciones', _external=True)) 
        elif response.status_code == 404:
            return render_template('404.html')
        else:
            return render_template('404.html') #deberia ser pagina de error 500
    except requests.RequestException:
        return render_template('404.html')     #deberia ser pagina de error 500
    
if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 