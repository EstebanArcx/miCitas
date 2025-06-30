from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from src.database.db import get_db
import os
from src.utils.auth_decorators import login_required

company_panel_bp = Blueprint('company_panel', __name__)

#Dashboard
@company_panel_bp.route('/company_panel/dashboard')
@login_required('company')
def company_dashboard():
    return render_template('company_panel/company_dashboard.html', head_title="Panel Empresa")


# settings, update data
@company_panel_bp.route('/company_panel/settings', methods=['GET', 'POST'])
@login_required('company')
def company_settings():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Obtener datos de la empresa actual
    cursor.execute("SELECT * FROM empresas WHERE id = %s", (session['user_id'],))
    company = cursor.fetchone()

    #Obtener los horarios actuales
    cursor.execute("""
        SELECT hora_inicio, hora_fin, turno FROM horarios_atencion 
        WHERE empresa_id = %s""", (session['user_id'],))
    schedules = cursor.fetchall()

    schedules_dict = {}
    for row in schedules:
        start_delta = row['hora_inicio']
        end_delta = row['hora_fin']

        # Extraer horas y minutos de timedelta
        start_hours = start_delta.seconds // 3600
        start_minutes = (start_delta.seconds % 3600) // 60
        end_hours = end_delta.seconds // 3600
        end_minutes = (end_delta.seconds % 3600) // 60

        schedules_dict[row['turno']] = {
            'start': f"{start_hours:02d}:{start_minutes:02d}",
            'end': f"{end_hours:02d}:{end_minutes:02d}"
        }

    if request.method == 'POST':

        # Datos básicos
        name = request.form['name']
        owner = request.form['owner']
        email = request.form['email']
        telephone = request.form['telephone']
        address = request.form['address']
        type = request.form['type']
        
        # Nueva contraseña si se proporciona
        new_password= request.form['password']
        
        # Horarios
        morning_start = request.form['morningStartTime']
        morning_end = request.form['morningEndtime']
        afternoon_start = request.form['afternoonStartTime']
        afternoon_end = request.form['afternoonEndTime']
        
        try:
            # Actualizar datos básicos
            cursor.execute("""
                UPDATE empresas 
                SET nombre = %s, propietario = %s, correo = %s, telefono = %s,
                    direccion = %s, tipo = %s
                WHERE id = %s
            """, (name, owner, email, telephone, address, type, session['user_id']))
            
            # Actualizar contraseña si se proporciona
            if new_password:
                hashed_password = generate_password_hash(new_password)
                cursor.execute("""
                    UPDATE empresas 
                    SET contrasena = %s
                    WHERE id = %s
                """, (hashed_password, session['user_id']))

            
            # Actualizar Horarios SOLO si no están en valores por defecto
            for turno, start, end, default_start, default_end in [
                ('mañana', morning_start, morning_end, "06:00", "06:00"),
                ('tarde', afternoon_start, afternoon_end, "12:00", "12:00")
            ]:
                if not (start == default_start and end == default_end):
                    cursor.execute("""
                        INSERT INTO horarios_atencion (empresa_id, hora_inicio, hora_fin, turno)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE hora_inicio = VALUES(hora_inicio), hora_fin = VALUES(hora_fin)
                    """, (session['user_id'], start, end, turno))

            
           
            db.commit()
            flash('Configuración actualizada exitosamente', 'success')
            return redirect(url_for('company_panel.company_settings'))
            
        except Exception as e:
            db.rollback()
            flash(f'Error al actualizar la configuración: {str(e)}', 'danger')

    return render_template('company_panel/company_settings.html', head_title="Configuración Empresa", company=company, schedules=schedules_dict)


#Images upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@company_panel_bp.route('/company_panel/update_images', methods=['POST'])
@login_required('company')
def update_images():
    
    
    profile_img = request.files.get('profile_img')
    company_img = request.files.get('company_img')

    upload_folder = os.path.join(current_app.root_path, 'static', 'imgs', 'company_imgs')
    os.makedirs(upload_folder, exist_ok=True)

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT img_perfil, img_negocio FROM empresas WHERE id = %s", (session['user_id'],))
    company = cursor.fetchone()

    if profile_img and allowed_file(profile_img.filename):
        if company['img_perfil']:  # Si hay una imagen previa
            old_path = os.path.join(upload_folder, company['img_perfil'])
            if os.path.exists(old_path):
                os.remove(old_path)

        filename = secure_filename(profile_img.filename)
        profile_img.save(os.path.join(upload_folder, filename))
        cursor.execute("UPDATE empresas SET img_perfil = %s WHERE id = %s", (filename, session['user_id']))

    if company_img and allowed_file(company_img.filename):
        if company['img_negocio']:  # Si hay una imagen previa
            old_path = os.path.join(upload_folder, company['img_negocio'])
            if os.path.exists(old_path):
                os.remove(old_path)

        filename = secure_filename(company_img.filename)
        company_img.save(os.path.join(upload_folder, filename))
        cursor.execute("UPDATE empresas SET img_negocio = %s WHERE id = %s", (filename, session['user_id']))

    db.commit()
    flash('Imágenes actualizadas correctamente', 'success')
    return redirect(url_for('company_panel.company_settings'))



