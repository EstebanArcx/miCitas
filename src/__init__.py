from flask import Flask
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()  # Carga las variables de .env

from src.database.db import close_db
from src.routes.auth import auth_bp
from src.routes.landing import landing_bp
from src.routes.company.company_panel import company_panel_bp
from src.routes.company.company_servicies import company_services_bp
from src.routes.company.appointments import company_appointments_bp


from src.routes.user.user_panel import user_panel_bp
from src.routes.user.user_settings import user_settings_bp
from src.routes.user.user_explore import user_explore_bp
from src.routes.user.user_explore_services import user_explore_services_bp 
from src.routes.user.schedule_appointment import schedule_appointment_bp 
from src.routes.user.appointments import user_appointments_bp 

def create_app():
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    app.secret_key = os.environ.get('SECRET_KEY')

    # Registrar Blueprints
    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp)


    app.register_blueprint(company_panel_bp)
    app.register_blueprint(company_services_bp)
    app.register_blueprint(company_appointments_bp)


    app.register_blueprint(user_panel_bp)
    app.register_blueprint(user_settings_bp)
    app.register_blueprint(user_explore_bp)
    app.register_blueprint(user_explore_services_bp )
    app.register_blueprint(schedule_appointment_bp )
    app.register_blueprint(user_appointments_bp )


    


    # Cierre automático de conexión a la base
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app
