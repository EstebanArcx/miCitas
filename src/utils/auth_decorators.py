from functools import wraps
from flask import session, redirect, url_for, flash

"""
Un decorador es una función que modifica el comportamiento de otra función, 
sin tener que cambiar su código.

wraps: mantiene el nombre y docstring original de la función decorada.

session: accede a los datos de sesión del usuario.

redirect, url_for, flash: para redirigir y mostrar mensajes.

"""
#Recibe un argumento type_session,'usuario' o 'empresa'.
# permite validar qué tipo de usuario tiene permiso para acceder a la ruta.
def login_required(type_session):
    
    def decorador(f): #Esta función recibe la función(ruta)
        
        @wraps(f) # @wraps(f) evita que se pierda el nombre y docstring 
        def wrapped(*args, **kwargs):# de la función original. Dentro de wrapped es donde se define la validación de sesión.
            if 'user_id' not in session or session.get('user_type') != type_session:
                return redirect(url_for('landing.index'))
            return f(*args, **kwargs)
        return wrapped
    
    return decorador