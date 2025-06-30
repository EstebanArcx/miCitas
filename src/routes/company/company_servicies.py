from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from src.utils.auth_decorators import login_required
from src.database.db import get_db

company_services_bp = Blueprint('company_services', __name__)

@company_services_bp.route('/company_panel/services', methods=['GET', 'POST'])
@login_required('company')
def company_services():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    empresa_id = session['user_id']

    # Obtener turnos configurados por la empresa
    cursor.execute("""
        SELECT turno FROM horarios_atencion
        WHERE empresa_id = %s
    """, (empresa_id,))
    turnos_configurados = [row['turno'] for row in cursor.fetchall()]

    # Definir turnos disponibles
    available_turns = []
    if 'mañana' in turnos_configurados:
        available_turns.append('mañana')
    if 'tarde' in turnos_configurados:
        available_turns.append('tarde')

    # Si envían el formulario (Registrar nuevo servicio)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        duracion = request.form['duracion']
        precio = request.form['precio']
        turnos = request.form.getlist('turnos[]')  # Lista de turnos seleccionados
        activo = request.form.get('activo', '1')

        if activo == '1':
            # Si está activo, debe tener al menos un turno seleccionado
            if not turnos:
                flash("Debes seleccionar al menos un turno disponible para el servicio activo.", "danger")
                return redirect(url_for('company_services.company_services'))

            # Validar que todos los turnos seleccionados estén permitidos
            for turno in turnos:
                if turno not in available_turns:
                    flash("Algunos de los turnos seleccionados no están permitidos según tus horarios configurados.", "danger")
                    return redirect(url_for('company_services.company_services'))

        try:
            # Insertar en servicios
            cursor.execute("""
                INSERT INTO servicios (empresa_id, nombre, descripcion, duracion, precio, activo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (empresa_id, nombre, descripcion, duracion, precio, activo))
            servicio_id = cursor.lastrowid

            # Insertar en servicio_turnos solo si está activo
            if activo == '1':
                for turno in turnos:
                    cursor.execute("""
                        INSERT INTO servicio_turnos (servicio_id, turno)
                        VALUES (%s, %s)
                    """, (servicio_id, turno))

            db.commit()
            flash("Servicio registrado correctamente.", "success")
        except Exception as e:
            db.rollback()
            flash(f"Error al registrar el servicio: {str(e)}", "danger")

        return redirect(url_for('company_services.company_services'))


    # Obtener servicios existentes
    cursor.execute("""
        SELECT s.*, GROUP_CONCAT(st.turno ORDER BY st.turno SEPARATOR ', ') AS turnos
        FROM servicios s
        LEFT JOIN servicio_turnos st ON s.id = st.servicio_id
        WHERE s.empresa_id = %s
        GROUP BY s.id
    """, (empresa_id,))
    servicios = cursor.fetchall()

    return render_template(
        "company_panel/company_services.html",
        head_title="Servicios",
        servicios=servicios,
        available_turns=available_turns
    )

@company_services_bp.route('/company_panel/edit_serv_company/<int:servicio_id>', methods=['GET', 'POST'])
@login_required('company')
def editar_servicio(servicio_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    empresa_id = session['user_id']

    # Obtener el servicio, verificar que pertenezca a la empresa
    cursor.execute("""
        SELECT * FROM servicios WHERE id = %s AND empresa_id = %s
    """, (servicio_id, empresa_id))
    servicio = cursor.fetchone()

    if not servicio:
        flash("Servicio no encontrado o no autorizado.", "danger")
        return redirect(url_for('company_services.company_services'))

    # Obtener turnos configurados por la empresa
    cursor.execute("""
        SELECT turno FROM horarios_atencion WHERE empresa_id = %s
    """, (empresa_id,))
    turnos_configurados = [row['turno'] for row in cursor.fetchall()]

    available_turns = []
    if 'mañana' in turnos_configurados:
        available_turns.append('mañana')
    if 'tarde' in turnos_configurados:
        available_turns.append('tarde')

    # Obtener turnos actuales del servicio
    cursor.execute("""
        SELECT turno FROM servicio_turnos WHERE servicio_id = %s
    """, (servicio_id,))
    turnos_actuales = [row['turno'] for row in cursor.fetchall()]

    # Si envían el formulario (POST)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        duracion = request.form['duracion']
        precio = request.form['precio']
        activo = request.form.get('activo', '1')

        turnos_seleccionados = request.form.getlist('turnos[]')

        # Validar turnos
        if activo == '1' and not turnos_seleccionados:
            flash("Debes seleccionar al menos un turno si el servicio está activo.", "danger")
            return redirect(request.url)

        for turno in turnos_seleccionados:
            if turno not in available_turns:
                flash("Has seleccionado un turno no permitido según tus horarios configurados.", "danger")
                return redirect(request.url)

        try:
            # Actualizar servicio
            cursor.execute("""
                UPDATE servicios SET nombre = %s, descripcion = %s, duracion = %s, precio = %s, activo = %s
                WHERE id = %s AND empresa_id = %s
            """, (nombre, descripcion, duracion, precio, activo, servicio_id, empresa_id))

            # Actualizar turnos
            cursor.execute("DELETE FROM servicio_turnos WHERE servicio_id = %s", (servicio_id,))
            if activo == '1':
                for turno in turnos_seleccionados:
                    cursor.execute("""
                        INSERT INTO servicio_turnos (servicio_id, turno)
                        VALUES (%s, %s)
                    """, (servicio_id, turno))

            db.commit()
            flash("Servicio actualizado correctamente.", "success")
            return redirect(url_for('company_services.company_services'))

        except Exception as e:
            db.rollback()
            flash(f"Error al actualizar el servicio: {str(e)}", "danger")
            return redirect(request.url)

    return render_template(
        'company_panel/edit_services.html',
        head_title="Editar Servicio",
        servicio={
            **servicio,
            'turnos': turnos_actuales
        },
        available_turns=available_turns
    )



# Delite Service
@company_services_bp.route('/elimin_serv_em', methods=['POST'])
@login_required('company')
def eliminar_servicio():
    db = get_db()
    cursor = db.cursor()
    servicio_id = request.form['id']
    empresa_id = session['user_id']

    try:
        # Eliminar primero los turnos asociados
        cursor.execute("""
            DELETE FROM servicio_turnos WHERE servicio_id = %s
        """, (servicio_id,))

        # Luego el servicio
        cursor.execute("""
            DELETE FROM servicios WHERE id = %s AND empresa_id = %s
        """, (servicio_id, empresa_id))
        
        db.commit()
        flash("Servicio eliminado correctamente.", "success")

    except Exception as e:
        db.rollback()
        flash(f"Error al eliminar el servicio: {str(e)}", "danger")

    return redirect(url_for('company_services.company_services'))
