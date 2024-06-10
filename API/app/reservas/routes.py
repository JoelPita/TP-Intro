import os
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# ---Crer Blueprint para reservas ---
reservas_bp = Blueprint('reservas', __name__)

# ---Crear las rutas con el blueprint---
@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    data = request.json
    query = text("""
        INSERT INTO Reservas (email_cliente, nombre_cliente, telefono_cliente, fecha_desde, fecha_hasta, 
            cantidad_habitaciones, cantidad_personas, metodo_pago, estado, precio_total, habitacion_id) 
        VALUES (:email_cliente, :nombre_cliente, :telefono_cliente, :fecha_desde, :fecha_hasta, :cantidad_habitaciones, 
            :cantidad_personas, :metodo_pago, :estado, :precio_total, :habitacion_id)
        """)
    
    try:
        engine = current_app.config['engine']
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
    
@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    estado = request.args.get('estado')
    if estado:
        query = text("SELECT * FROM Reservas WHERE estado = :estado")
        params = {'estado': estado}
    else:
        query = text("SELECT * FROM Reservas")
        params = {}

    try:
        engine = current_app.config['engine']
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
    


@reservas_bp.route('/<int:id>/confirm', methods=['PUT'])
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
        engine = current_app.config['engine']
        conn = engine.connect()
        conn.execute(query, {
            'estado': estado,
            'motivo_rechazo': motivo_rechazo,
            'id': id
        })

        send_email(data['email_cliente'], estado, motivo_rechazo)

        conn.commit()
        conn.close()
        
        #TO DO: IMPLEMENTAR ENVIO DE MAIL

        return jsonify({"success": True, "message": "Reserva actualizada correctamente"}), 200
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500

def send_email(email, estado, motivo_rechazo):
    from_email = 'from_email@example.com'  # Cambia esto por tu correo de envío
    subject = f'Su reserva ha sido {estado}'
    if estado == 'rechazada':
        content = f'<p>Lo sentimos, su reserva ha sido rechazada. Motivo: {motivo_rechazo}</p>'
    else:
        content = '<p>¡Felicidades! Su reserva ha sido aceptada.</p>'
    
    message = Mail(
        from_email=from_email,
        to_emails=email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
