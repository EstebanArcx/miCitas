from flask import Blueprint, render_template
from src.utils.auth_decorators import login_required
from src.database.db import get_db

user_explore_bp = Blueprint('user_explore', __name__)

@user_explore_bp.route('/user_panel/explore')
@login_required('user')
def user_explore():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Traer todas las empresas
    cursor.execute("""
        SELECT id, nombre, tipo, direccion, img_perfil, img_negocio
        FROM empresas
    """)
    empresas = cursor.fetchall()

    return render_template('user_panel/user_explore.html', head_title="Explorar Empresas", empresas=empresas)
