CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(60) NOT NULL,
        correo VARCHAR(60) UNIQUE NOT NULL,
        tipo VARCHAR(20) NOT NULL,
        telefono VARCHAR(20),
        direccion VARCHAR(60),
        propietario VARCHAR(60),
        contrasena TEXT NOT NULL,
        img_perfil TEXT,
        img_negocio TEXT
        
    );
    
CREATE TABLE IF NOT EXISTS horarios_atencion (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        empresa_id INTEGER NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        turno TEXT CHECK (turno IN ('mañana', 'tarde', 'noche')),
        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
    );
    
CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        nombre VARCHAR(60) NOT NULL,
        correo VARCHAR(60) UNIQUE NOT NULL,
        telefono VARCHAR(20),
        contrasena TEXT NOT NULL,
        img_perfil TEXT
    );
    
CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
        empresa_id INTEGER NOT NULL,
        nombre VARCHAR(60) NOT NULL,
        descripcion TEXT,
        duracion INTEGER NOT NULL, -- en minutos
        precio REAL NOT NULL,
        activo BOOLEAN DEFAULT 1,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

CREATE TABLE IF NOT EXISTS servicio_turnos (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        servicio_id INTEGER NOT NULL,
        turno TEXT NOT NULL CHECK (turno IN ('mañana', 'tarde', 'noche')),
        FOREIGN KEY (servicio_id) REFERENCES servicios(id)
    );


CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    usuario_id INTEGER NOT NULL,
    empresa_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado TEXT DEFAULT 'pendiente',  -- otras opciones: 'cancelada', 'completada'
    notas TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

CREATE TABLE IF NOT EXISTS comentarios_app (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        contenido TEXT NOT NULL,
        fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
        autor_tipo TEXT NOT NULL CHECK (autor_tipo IN ('usuario', 'empresa')),
        autor_id INTEGER NOT NULL
    );
    
ALTER TABLE horarios_atencion
ADD CONSTRAINT unique_empresa_turno UNIQUE (empresa_id, turno);
    
    
