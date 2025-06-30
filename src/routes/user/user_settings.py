from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from src.database.db import get_db
import os
from src.utils.auth_decorators import login_required

user_settings_bp = Blueprint('user_settings', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Configuración general
@user_settings_bp.route('/user_panel/settings', methods=['GET', 'POST'])
@login_required('user')
def user_settings():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        new_password = request.form['password']

        try:
            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s, correo = %s, telefono = %s
                WHERE id = %s
            """, (name, email, telephone, user_id))

            if new_password:
                hashed_password = generate_password_hash(new_password)
                cursor.execute("""
                    UPDATE usuarios
                    SET contrasena = %s
                    WHERE id = %s
                """, (hashed_password, user_id))

            db.commit()
            flash('Configuración actualizada exitosamente.', 'success')
            return redirect(url_for('user_settings.user_settings'))

        except Exception as e:
            db.rollback()
            flash(f'Error al actualizar configuración: {str(e)}', 'danger')

    return render_template('user_panel/user_settings.html', head_title="Configuración Panel Usuario", user=user)


# Actualizar imagen de perfil
@user_settings_bp.route('/user_panel/update_image', methods=['POST'])
@login_required('user')
def update_image():
    img_perfil = request.files.get('img_perfil')
    user_id = session['user_id']

    upload_folder = os.path.join(current_app.root_path, 'static', 'imgs', 'user_imgs')
    os.makedirs(upload_folder, exist_ok=True)

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT img_perfil FROM usuarios WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if img_perfil and allowed_file(img_perfil.filename):
        if user['img_perfil']:
            old_path = os.path.join(upload_folder, user['img_perfil'])
            if os.path.exists(old_path):
                os.remove(old_path)

        filename = secure_filename(img_perfil.filename)
        img_perfil.save(os.path.join(upload_folder, filename))

        cursor.execute("UPDATE usuarios SET img_perfil = %s WHERE id = %s", (filename, user_id))
        db.commit()
        flash('Imagen de perfil actualizada correctamente.', 'success')
    else:
        flash('Debes seleccionar una imagen válida.', 'danger')

    return redirect(url_for('user_settings.user_settings'))
