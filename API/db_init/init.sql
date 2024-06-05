CREATE DATABASE IF NOT EXISTS flaskdb;
USE flaskdb;

CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email_cliente VARCHAR(255) NOT NULL,
    nombre_cliente VARCHAR(255) NOT NULL,
    telefono_cliente VARCHAR(20),
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE NOT NULL,
    cantidad_habitaciones INT NOT NULL,
    cantidad_personas INT NOT NULL,
    metodo_pago VARCHAR(50),
    estado VARCHAR(50),
    motivo_rechazo VARCHAR(250)
);

CREATE TABLE IF NOT EXISTS Reseñas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_autor VARCHAR(50) NOT NULL,
    texto VARCHAR(255) NOT NULL,
    mostrar BOOLEAN NOT NULL
);