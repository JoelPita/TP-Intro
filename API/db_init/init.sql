CREATE DATABASE IF NOT EXISTS flaskdb;
USE flaskdb;

CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(20),
    precio_noche DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_cliente VARCHAR(100) NOT NULL,
    nombre_cliente VARCHAR(80) NOT NULL,
    telefono_cliente VARCHAR(20),
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE NOT NULL,
    cantidad_habitaciones INT NOT NULL,
    cantidad_personas INT NOT NULL,
    metodo_pago VARCHAR(50),
    estado VARCHAR(50),
    motivo_rechazo VARCHAR(150),
    precio_total DECIMAL(10, 2),
    habitacion_id INT,
    FOREIGN KEY (habitacion_id) REFERENCES Habitaciones(id)
);

CREATE TABLE IF NOT EXISTS Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_autor VARCHAR(80) NOT NULL,
    texto VARCHAR(150) NOT NULL,
    visible BOOLEAN NOT NULL
);