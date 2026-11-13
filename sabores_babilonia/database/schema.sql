USE sabores_babilonia;

DROP TABLE IF EXISTS detalle_pedido;
DROP TABLE IF EXISTS pagos;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefono VARCHAR(15) NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'admin') DEFAULT 'cliente',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_ingreso DATETIME NULL
);

CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'pagado', 'enviado', 'entregado', 'cancelado') DEFAULT 'pendiente',
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE detalle_pedido (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    tarjeta_encriptada BLOB NULL,
    ultimos_4_digitos CHAR(4) NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido)
);

CREATE INDEX idx_pagos_ultimos4 ON pagos(ultimos_4_digitos);

DELIMITER //
CREATE TRIGGER audit_pedidos_delete
BEFORE DELETE ON pedidos
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_sistema (usuario_bd, accion, tabla_afectada, registro_id, valor_anterior)
    VALUES (
        USER(), 
        'DELETE', 
        'pedidos', 
        OLD.id_pedido, 
        CONCAT('Usuario: ', OLD.id_usuario, ' | Total: ', OLD.total, ' | Estado: ', OLD.estado)
    );
END//
DELIMITER ;

CREATE USER IF NOT EXISTS 'web_sabores_user'@'127.0.0.1' IDENTIFIED BY 'SaboresWeb2026*';
GRANT SELECT, INSERT, UPDATE ON sabores_babilonia.* TO 'web_sabores_user'@'127.0.0.1';
GRANT SELECT, INSERT, UPDATE ON sabores_babilonia.* TO 'web_sabores_user'@'localhost';
FLUSH PRIVILEGES;
