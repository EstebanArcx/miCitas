from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session
from src.database.db import get_db
from src.utils.auth_decorators import login_required
from datetime import datetime

company_appointments_bp = Blueprint('company_appointments', __name__)

@company_appointments_bp.route('/company_panel/appointments')
@login_required('company')
def company_appointments():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.estado, c.notas,
               s.nombre AS servicio_nombre, s.duracion,
               u.nombre AS usuario_nombre, u.telefono AS usuario_telefono
        FROM citas c
        JOIN servicios s ON c.servicio_id = s.id
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE c.empresa_id = %s
        ORDER BY c.fecha DESC, c.hora DESC
    """, (session['user_id'],))

    citas = cursor.fetchall()

    return render_template('company_panel/company_appointments.html',
                           head_title="Agenda",
                           citas=citas)


@company_appointments_bp.route('/company_panel/appointments/cancel/<int:cita_id>')
@login_required('company')
def cancel_appointment(cita_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE citas
        SET estado = 'cancelada'
        WHERE id = %s AND empresa_id = %s AND estado = 'pendiente'
    """, (cita_id, session['user_id']))

    if cursor.rowcount > 0:
        db.commit()
        flash("Cita cancelada exitosamente.", "success")
    else:
        flash("No se pudo cancelar la cita. Verifica el estado.", "danger")

    return redirect(url_for('company_appointments.company_appointments'))


@company_appointments_bp.route('/company_panel/delete_appointment/<int:cita_id>')
@login_required('company')
def delete_appointment(cita_id):
    db = get_db()
    cursor = db.cursor()

    try:
        # Elimina la cita definitivamente
        cursor.execute("""
            DELETE FROM citas 
            WHERE id = %s AND empresa_id = %s
        """, (cita_id, session['user_id']))
        db.commit()
        flash("Cita eliminada permanentemente.", "success")
    except Exception as e:
        db.rollback()
        print(e)
        flash("Ocurrió un error al eliminar la cita.", "danger")

    return redirect(url_for('company_appointments.company_appointments'))