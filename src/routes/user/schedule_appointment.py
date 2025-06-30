from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from src.utils.auth_decorators import login_required
from src.database.db import get_db
from datetime import datetime, timedelta

schedule_appointment_bp = Blueprint('schedule_appointment', __name__)

# Vista principal para reservar cita
@schedule_appointment_bp.route('/book_appointment/<int:service_id>', methods=['GET', 'POST'])
@login_required('user')
def schedule_appointment(service_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Consultar datos del servicio
    cursor.execute("""
        SELECT s.id, s.nombre, s.descripcion, s.duracion, s.precio, e.id AS empresa_id, e.nombre AS empresa_nombre
        FROM servicios s
        JOIN empresas e ON s.empresa_id = e.id
        WHERE s.id = %s AND s.activo = 1
    """, (service_id,))
    service = cursor.fetchone()

    if not service:
        flash('Servicio no encontrado o inactivo.', 'danger')
        return redirect(url_for('user_explore.user_explore'))

    # Consultar turnos configurados para el servicio
    cursor.execute("SELECT turno FROM servicio_turnos WHERE servicio_id = %s", (service_id,))
    turnos_result = cursor.fetchall()
    available_turns = [t['turno'] for t in turnos_result]
    turnos_str = ", ".join(available_turns) if available_turns else "Sin turnos configurados"

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        notas = request.form.get('notas', '')

        if not fecha or not hora:
            flash('Debes seleccionar un día y una hora.', 'danger')
            return redirect(request.url)

        try:
            # Registrar la cita
            cursor.execute("""
                INSERT INTO citas (usuario_id, empresa_id, servicio_id, fecha, hora, notas)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (session['user_id'], service['empresa_id'], service['id'], fecha, hora, notas))
            db.commit()

            flash('¡Cita reservada exitosamente!', 'success')
            return redirect(url_for('schedule_appointment.schedule_appointment', service_id=service['id']))

        except Exception as e:
            print(e)
            db.rollback()
            flash('Error al reservar la cita.', 'danger')

    return render_template('user_panel/user_schedule_appointment.html',
                           head_title="Reservar Cita",
                           service=service,
                           turno=turnos_str)


# Endpoint que devuelve las horas disponibles según el día seleccionado
@schedule_appointment_bp.route('/user_panel/get_available_hours/<int:service_id>')
@login_required('user')
def get_available_hours(service_id):
    fecha = request.args.get('fecha')
    if not fecha:
        return jsonify([])

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener datos del servicio
    cursor.execute("""
        SELECT s.duracion, e.id AS empresa_id
        FROM servicios s
        JOIN empresas e ON s.empresa_id = e.id
        WHERE s.id = %s
    """, (service_id,))
    service = cursor.fetchone()

    if not service:
        return jsonify([])

    duracion = service['duracion']
    empresa_id = service['empresa_id']

    # Turnos configurados para el servicio
    cursor.execute("SELECT turno FROM servicio_turnos WHERE servicio_id = %s", (service_id,))
    turnos_result = cursor.fetchall()
    turnos_servicio = [t['turno'] for t in turnos_result]

    if not turnos_servicio:
        return jsonify([])

    # Construcción segura del IN dinámico
    placeholders = ','.join(['%s'] * len(turnos_servicio))
    query = f"""
        SELECT hora_inicio, hora_fin
        FROM horarios_atencion
        WHERE empresa_id = %s AND turno IN ({placeholders})
    """

    params = [empresa_id] + turnos_servicio
    cursor.execute(query, params)
    horarios = cursor.fetchall()

    if not horarios:
        return jsonify([])

    # Horas ocupadas ya reservadas para ese día
    cursor.execute("""
        SELECT hora
        FROM citas
        WHERE servicio_id = %s AND fecha = %s
    """, (service_id, fecha))
    citas_existentes = [str(c['hora']) for c in cursor.fetchall()]

    horas_disponibles = []

    for h in horarios:
        inicio = datetime.strptime(str(h['hora_inicio']), "%H:%M:%S")
        fin = datetime.strptime(str(h['hora_fin']), "%H:%M:%S")

        hora_actual = inicio
        while hora_actual + timedelta(minutes=duracion) <= fin:
            hora_str = hora_actual.strftime("%H:%M:%S")
            if hora_str not in citas_existentes:
                horas_disponibles.append(hora_actual.strftime("%H:%M"))
            hora_actual += timedelta(minutes=duracion)

    return jsonify(horas_disponibles)
