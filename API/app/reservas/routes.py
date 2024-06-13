import os
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

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
    query_update = text("""
        UPDATE Reservas 
        SET estado = :estado, motivo_rechazo = :motivo_rechazo
        WHERE id = :id
        """)
    
    query_select = text("""
        SELECT R.email_cliente, R.nombre_cliente, R.telefono_cliente, R.fecha_desde, R.fecha_hasta, 
                R.cantidad_habitaciones, R.cantidad_personas, R.metodo_pago, R.precio_total, H.nombre
        FROM Reservas R
        INNER JOIN Habitaciones H ON R.habitacion_id = H.id
        WHERE R.id = :id
        """)
        
    try:
        engine = current_app.config['engine']
        conn = engine.connect()

        result_get_reserva = conn.execute(query_select, {'id': id})

        if result_get_reserva.rowcount == 0:
            conn.close()
            return jsonify({"success": False, "message": "Reserva no encontrada"}), 404
        
        # Actualizar el estado de la reserva
        conn.execute(query_update, {
            'estado': estado,
            'motivo_rechazo': motivo_rechazo,
            'id': id
        })

        conn.commit()
        conn.close()
        
        
        reserva = result_get_reserva.fetchone()
        reserva_data = {
            'email_cliente': reserva[0],
            'nombre_cliente': reserva[1],
            'telefono_cliente': reserva[2],
            'fecha_desde': reserva[3],
            'fecha_hasta': reserva[4],
            'cantidad_habitaciones': reserva[5],
            'cantidad_personas': reserva[6],
            'metodo_pago': reserva[7],
            'precio_total': reserva[8],
            'nombre_habitacion': reserva[9]
        }

        subject = f'Hotel del Glaciar | Su reserva ha sido {estado}'
        if estado == 'rechazada':
            content = f"""
                <p>Lo sentimos, su reserva ha sido rechazada.</p>
                <p>Motivo: {motivo_rechazo}</p>
                <p>Detalles de la reserva:</p>
                <p>Nombre: {reserva_data['nombre_cliente']}</p>
                <p>Teléfono: {reserva_data['telefono_cliente']}</p>
                <p>Fecha Desde: {reserva_data['fecha_desde']}</p>
                <p>Fecha Hasta: {reserva_data['fecha_hasta']}</p>
                <p>Cantidad de Habitaciones: {reserva_data['cantidad_habitaciones']}</p>
                <p>Tipo de habitacion: {reserva_data['nombre_habitacion']}</p>
                <p>Cantidad de Personas: {reserva_data['cantidad_personas']}</p>
                <p>Precio Total: {reserva_data['precio_total']}</p>
            """
        else:
            content = f"""
                <p>¡Felicidades! Su reserva ha sido aceptada.</p>
                <p>Detalles de la reserva:</p>
                <p>Nombre: {reserva_data['nombre_cliente']}</p>
                <p>Teléfono: {reserva_data['telefono_cliente']}</p>
                <p>Fecha Desde: {reserva_data['fecha_desde']}</p>
                <p>Fecha Hasta: {reserva_data['fecha_hasta']}</p>
                <p>Cantidad de Habitaciones: {reserva_data['cantidad_habitaciones']}</p>
                <p>Tipo de habitacion: {reserva_data['nombre_habitacion']}</p>
                <p>Cantidad de Personas: {reserva_data['cantidad_personas']}</p>
                <p>Precio Total: {reserva_data['precio_total']}</p>
                <p>Metodo de Pago: {reserva_data['metodo_pago']}</p>
            """
        
        send_email(reserva_data['email_cliente'], subject, content)
        return jsonify({"success": True, "message": "Reserva actualizada correctamente"}), 200
    
    except SQLAlchemyError as e:
        error = str(e.__cause__)
        conn.close()
        return jsonify({"success": False, "message": error}), 500

def send_email(to_email, subject, content):
    from_email = 'mriveiro@fi.uba.ar'
    
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(f'Status Code: {response.status_code}')
        logging.info(f'Response Body: {response.body}')
        logging.info(f'Response Headers: {response.headers}')
    except Exception as e:
        logging.error(f'Error: {str(e)}')