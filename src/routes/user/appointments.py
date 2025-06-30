from flask import Blueprint, render_template, session
from src.utils.auth_decorators import login_required
from src.database.db import get_db

user_appointments_bp = Blueprint('user_appointments', __name__)

@user_appointments_bp.route('/user_panel/appointments')
@login_required('user')
def user_appointments():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.estado, c.notas,
               s.nombre AS servicio_nombre, s.duracion,
               e.nombre AS empresa_nombre, e.tipo
        FROM citas c
        JOIN servicios s ON c.servicio_id = s.id
        JOIN empresas e ON c.empresa_id = e.id
        WHERE c.usuario_id = %s
        ORDER BY c.fecha DESC, c.hora DESC
    """, (session['user_id'],))

    citas = cursor.fetchall()

    return render_template('user_panel/user_appointments.html', head_title="Tus Citas", citas=citas)
