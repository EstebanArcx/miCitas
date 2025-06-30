from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from src.database.db import get_db

auth_bp = Blueprint('auth', __name__)


# Choose Role
@auth_bp.route("/choose_rol")
def choose_rol():
    #Captura el parámetro 'accion' de la URL, si no existe, usa 'login' por defecto
    accion = request.args.get("accion", "login")
    return render_template("choose_rol.html", accion=accion, head_title="Elegir Rol")


# register a company
@auth_bp.route("/company_registration", methods=["GET", "POST"])
def company_registration():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        type = request.form['type']
        password = generate_password_hash(request.form['password'])

        db = get_db()
        cursor = db.cursor()

        # Verifica que el correo no exista ni en empresas ni en usuarios
        cursor.execute("""
            SELECT 1 FROM empresas WHERE correo = %s 
            UNION 
            SELECT 1 FROM usuarios WHERE correo = %s
        """, (email, email))
        correo_existente = cursor.fetchone() #Si no encuentra otro correo devuelve None

        if correo_existente:
            flash("Correo ya registrado.", "danger")
            return redirect(url_for('auth.company_registration'))

        try:
            cursor.execute("""
                INSERT INTO empresas (nombre, correo, tipo, contrasena)
                VALUES (%s, %s, %s, %s)
            """, (name, email, type, password))
            db.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.rollback()
            flash(f'Error al registrar la empresa: {str(e)}', 'danger')

    return render_template("company_registration.html", mode="company", head_title="Registro Empresa")


# register a user
@auth_bp.route("/user_registration", methods=["GET", "POST"])
def user_registration():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = generate_password_hash(request.form['password'])
        

        db = get_db()
        cursor = db.cursor()

        # Verifica si el correo ya existe en usuarios o empresas
        cursor.execute("""
            SELECT 1 FROM usuarios WHERE correo = %s
            UNION
            SELECT 1 FROM empresas WHERE correo = %s
        """, (email, email))
        correo_existente = cursor.fetchone()

        if correo_existente:
            flash("Correo ya registrado.", "danger")
            return redirect(url_for('auth.user_registration'))

        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, telefono, contrasena)
                VALUES (%s, %s, %s, %s)
            """, (name, email, phone, password))
            db.commit()
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login_usuario'))  # Asegúrate de tener esta ruta
            
        except Exception as e:
            db.rollback()
            flash(f'Error al registrar usuario: {str(e)}', 'danger')
            return redirect(url_for('auth.user_registration'))

    return render_template("user_registration.html", mode="user", head_title="Registro Usuario")


#login company-user
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Buscar en empresas primero
        cursor.execute("SELECT * FROM empresas WHERE correo = %s", (email,))
        company = cursor.fetchone()

        if company and check_password_hash(company['contrasena'], password):
            session.clear()
            session['user_id'] = company['id']
            session['user_type'] = 'company'
            session['username'] = company['nombre']
            session['user_img'] = company['img_perfil']
            flash('Credenciales Correctas!...Cargando', 'success')
            return redirect(url_for('auth.login', redirect_url=url_for('company_panel.company_dashboard')))  

        # Si no es empresa, buscar en usuarios
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['contrasena'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_type'] = 'user'
            session['username'] = user['nombre']
            session['user_img'] = user['img_perfil']
            flash('Credenciales Correctas!...Cargando', 'success')
            return redirect(url_for('auth.login', redirect_url=url_for('user_panel.user_dashboard'))) 

        flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html', mode="login", head_title="Iniciar Sesion")

#logout company-user
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('landing.index'))