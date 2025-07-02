# 🗓️ Sistema de Gestión de Citas y Empresas

Este es un proyecto personal desarrollado con Python (Flask) y MySQL, que permite la gestión de citas entre usuarios y empresas, así como la administración de servicios, horarios y comentarios. El sistema está pensado para ser una base extensible para soluciones de reservas y gestión de empresas.

## ⚙️ Funcionalidades principales

- Registro y autenticación de usuarios y empresas.
- Gestión de empresas, servicios y horarios de atención.
- Reserva y gestión de citas entre usuarios y empresas.
- Paneles diferenciados para usuarios y empresas.
- Seguridad en el manejo de contraseñas y sesiones.
- Sistema de comentarios para usuarios y empresas. (A implementar)

## 🗂️ Estructura del proyecto

- `src/`: Código fuente principal.
  - `routes/`: Rutas Flask para autenticación y otras funcionalidades.
  - `database/`: Conexión y estructura de la base de datos.
  - `templates/`: Plantillas HTML para la interfaz.
  - `static/`: Archivos estáticos (JS, CSS, imágenes).
  - `utils/`: Utilidades y decoradores para autenticación.
- `db_structure.sql`: Script SQL para crear la estructura inicial de la base de datos.
- `.env_example`: Ejemplo de archivo de variables de entorno.
- `requirements.txt`: Dependencias Python.
- `package.json` y `package-lock.json`: Dependencias para recursos front-end (si usas Node.js para assets).

## 🧹 Dependencias principales

### 🐍 Python

- Flask
- mysql-connector-python
- python-dotenv

Instálalas con:

```bash
pip install -r requirements.txt
```

### 🎨 Node.js y Tailwind CSS

Este proyecto utiliza [Tailwind CSS](https://tailwindcss.com/) versión 3.4.17 para los estilos, implementado mediante Tailwind CLI.

#### 🛠️ Instalación de Tailwind CLI

Instala Tailwind CLI de forma global o como dependencia de desarrollo:

```bash
npm install -D tailwindcss@3.4.17
```

O globalmente:

```bash
npm install -g tailwindcss@3.4.17
```

#### 🎨 Generar los estilos

Para compilar los estilos de Tailwind ejecuta:

```bash
tailwindcss -i ./src/static/css/input.css -o ./src/static/css/output.css --watch
```

(ajusta las rutas según tu estructura de carpetas)

## ⚒️ Configuración inicial

1. **Clona el repositorio:**

   ```bash
   git clone <URL-del-repo>
   cd <nombre-del-repo>
   ```

2. **Crea tu archivo `.env`** (basado en `.env_example`):

   ```bash
   cp .env_example .env
   ```

   Completa los valores necesarios (`SECRET_KEY`, `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).

3. **Instala las dependencias de Python:**

   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Instala dependencias de Node.js:**

   ```bash
   npm install
   ```

5. **Crea la base de datos:**

   - Asegúrate de tener MySQL corriendo.
   - Ejecuta el script de estructura:
   
     ```bash
     mysql -u <usuario> -p <nombre_bd> < src/database/db_structure.sql
     ```

## 🚀 Ejecución local

Puedes ejecutar el proyecto con:

```bash
python run.py
```

O, si usas Flask directamente:

```bash
export FLASK_APP=run.py
flask run
```

## 📄 Licencia

Este repositorio está bajo la licencia **Apache 2.0**. Puedes utilizar, modificar y distribuir este material libremente, incluso para fines comerciales, siempre que mantengas los avisos de copyright y de licencia correspondientes. Si compartes o distribuyes este trabajo, se agradece que cites este repositorio como fuente.

## 📧 Contacto

Si tienes alguna duda o sugerencia, puedes contactarme a través de:

<a href="https://github.com/EstebanArcx" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-%2312100E.svg?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</a>
