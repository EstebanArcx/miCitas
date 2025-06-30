from flask import Blueprint, render_template, g
from src.utils.auth_decorators import login_required
from src.database.db import get_db

user_explore_services_bp = Blueprint('user_explore_services', __name__)

@user_explore_services_bp.route('/user_panel/explore/services/<int:empresa_id>')
@login_required('user')
def user_explore_services(empresa_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener datos de la empresa
    cursor.execute("SELECT * FROM empresas WHERE id = %s", (empresa_id,))
    empresa = cursor.fetchone()

    if not empresa:
        return "Negocio no encontrado", 404

    # Obtener los servicios activos de esa empresa
    cursor.execute("""
            SELECT s.id, s.nombre AS name, s.descripcion AS description, s.duracion AS duration, 
                s.precio AS price, GROUP_CONCAT(st.turno SEPARATOR '/') AS turnos
            FROM servicios s
            LEFT JOIN servicio_turnos st ON s.id = st.servicio_id
            WHERE s.empresa_id = %s AND s.activo = 1
            GROUP BY s.id
        """, (empresa_id,))
    services = cursor.fetchall()


    # Obtener horarios de atención
    cursor.execute("""
        SELECT turno, hora_inicio, hora_fin
        FROM horarios_atencion
        WHERE empresa_id = %s
    """, (empresa_id,))
    horarios = cursor.fetchall()

    horarios_dict = {}
    for h in horarios:
        start_hours = h['hora_inicio'].seconds // 3600
        start_minutes = (h['hora_inicio'].seconds % 3600) // 60
        end_hours = h['hora_fin'].seconds // 3600
        end_minutes = (h['hora_fin'].seconds % 3600) // 60
        horarios_dict[h['turno']] = f"{start_hours:02d}:{start_minutes:02d} - {end_hours:02d}:{end_minutes:02d}"

    return render_template('user_panel/user_explore_services.html',
                           head_title=f"Servicios de {empresa['nombre']}",
                           empresa=empresa,
                           horarios=horarios_dict,
                           services=services)
