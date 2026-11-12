-- Base de datos de Sabores de Babilonia
CREATE DATABASE IF NOT EXISTS sabores_babilonia
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sabores_babilonia;

CREATE TABLE IF NOT EXISTS usuarios (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(100) NOT NULL,
  email         VARCHAR(150) NOT NULL UNIQUE,
  telefono      VARCHAR(30)  NULL,
  password_hash VARCHAR(255) NOT NULL,
  rol           ENUM('cliente','admin') NOT NULL DEFAULT 'cliente',
  creado_en     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ultimo_ingreso TIMESTAMP NULL
) ENGINE=InnoDB;

-- Usuario de aplicación con permisos mínimos (cambia la contraseña)
-- CREATE USER 'sdb_user'@'localhost' IDENTIFIED BY 'cambia_esta_contrasena';
-- GRANT SELECT, INSERT, UPDATE ON sabores_babilonia.* TO 'sdb_user'@'localhost';
-- FLUSH PRIVILEGES;
