-- =======================
-- Estructura base holding
-- =======================

CREATE DATABASE IF NOT EXISTS holding_rrhh;
USE holding_rrhh;

-- Empresas del holding
CREATE TABLE IF NOT EXISTS empresas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    rut VARCHAR(12) NOT NULL UNIQUE
);

-- Usuarios Portal
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    img TEXT,
    full_name VARCHAR(150),
    disabled BOOLEAN DEFAULT FALSE
);

-- Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    rut VARCHAR(12) NOT NULL UNIQUE,
    fecha_nacimiento DATE,
    direccion TEXT
);

-- Contratos laborales
CREATE TABLE IF NOT EXISTS contratos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT NOT NULL,
    empresa_id INT NOT NULL,
    tipo ENUM('INDEFINIDO','PLAZO_FIJO') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_termino DATE,
    sueldo_base INT NOT NULL,
    afp_id INT,
    salud_id INT,
    afc_id INT,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id),
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

-- AFP (previsión)
CREATE TABLE IF NOT EXISTS afp (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tasas AFP históricas
CREATE TABLE IF NOT EXISTS afp_tasas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    afp_id INT NOT NULL,
    tasa DECIMAL(5,2) NOT NULL,         -- ej. 10.5
    vigente_desde DATE NOT NULL,
    vigente_hasta DATE,
    FOREIGN KEY (afp_id) REFERENCES afp(id)
);

-- Salud (Fonasa / Isapre)
CREATE TABLE IF NOT EXISTS salud (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tasas Salud históricas
CREATE TABLE IF NOT EXISTS salud_tasas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    salud_id INT NOT NULL,
    tasa DECIMAL(5,2) NOT NULL,          -- normalmente 7.0
    vigente_desde DATE NOT NULL,
    vigente_hasta DATE,
    FOREIGN KEY (salud_id) REFERENCES salud(id)
);

-- AFC (seguro de cesantía, solo indefinidos)
CREATE TABLE IF NOT EXISTS afc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tasas AFC históricas
CREATE TABLE IF NOT EXISTS afc_tasas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    afc_id INT NOT NULL,
    tasa_trabajador DECIMAL(5,2) NOT NULL,
    tasa_empleador DECIMAL(5,2) NOT NULL,
    vigente_desde DATE NOT NULL,
    vigente_hasta DATE,
    FOREIGN KEY (afc_id) REFERENCES afc(id)
);

-- Liquidaciones mensuales
CREATE TABLE IF NOT EXISTS liquidaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contrato_id INT NOT NULL,
    periodo YEAR(4) NOT NULL,
    mes TINYINT NOT NULL,
    sueldo_base DECIMAL(12,2) NOT NULL,
    horas_extra DECIMAL(12,2) DEFAULT 0,
    gratificacion DECIMAL(12,2) DEFAULT 0,
    total_imponible DECIMAL(12,2) DEFAULT 0,
    total_descuentos DECIMAL(12,2) DEFAULT 0,
    liquido_a_pagar DECIMAL(12,2) DEFAULT 0,
    FOREIGN KEY (contrato_id) REFERENCES contratos(id)
);

USE holding_rrhh;


INSERT INTO usuarios (email, password, img, full_name, disabled) VALUES 
('admin@gmail.com', 'MiPass123.', 'H.png', 'Felipe Piltov', FALSE);


INSERT INTO salud (id, nombre) VALUES
(1, 'FONASA'),
(2, 'Isapre Banmédica'),
(3, 'Isapre Colmena'),
(4, 'Isapre Consalud'),
(5, 'Isapre Cruz Blanca'),
(6, 'Isapre Nueva Masvida'),
(7, 'Isapre Vida Tres');

INSERT INTO afp (id, nombre) VALUES
(1, 'AFP Capital'),
(2, 'AFP Cuprum'),
(3, 'AFP Habitat'),
(4, 'AFP Modelo'),
(5, 'AFP PlanVital'),
(6, 'AFP Provida'),
(7, 'AFP Uno');

INSERT INTO afp_tasas (afp_id, tasa, vigente_desde) VALUES
(1, 11.44, '2025-01-01'),  -- AFP Capital
(2, 11.63, '2025-01-01'),  -- AFP Cuprum
(3, 10.50, '2025-01-01'),  -- AFP Habitat
(4, 11.45, '2025-01-01'),  -- AFP Modelo
(5, 10.77, '2025-01-01'),  -- AFP PlanVital
(6, 10.80, '2025-01-01'),  -- AFP Provida
(7, 10.96, '2025-01-01');  -- AFP Uno

-- Todas las instituciones de salud cotizan mínimo 7%
INSERT INTO salud_tasas (salud_id, tasa, vigente_desde) VALUES
(1, 7.00, '2025-01-01'),  -- FONASA
(2, 7.00, '2025-01-01'),  -- Isapre Banmédica
(3, 7.00, '2025-01-01'),  -- Isapre Colmena
(4, 7.00, '2025-01-01'),  -- Isapre Consalud
(5, 7.00, '2025-01-01'),  -- Isapre Cruz Blanca
(6, 7.00, '2025-01-01'),  -- Isapre Nueva Masvida
(7, 7.00, '2025-01-01');  -- Isapre Vida Tres

-- Para contratos indefinidos: trabajador 0.6%, empleador 2.4% / Para plazo fijo el empleador paga el 3%
INSERT INTO afc (nombre) VALUES ('AFC Chile');
INSERT INTO afc_tasas (afc_id, tasa_trabajador, tasa_empleador, vigente_desde) VALUES
(1, 0.60, 2.40, '2025-01-01');
-- AFC contrato plazo fijo
INSERT INTO afc_tasas (afc_id, tasa_trabajador, tasa_empleador, vigente_desde) VALUES
(1, 0.00, 3.00, '2025-01-01');


INSERT INTO empleados (nombres, apellidos, rut, fecha_nacimiento, direccion) VALUES
('Juan', 'Pérez Soto', '11.111.111-1', '1990-04-15', 'Calle Falsa 123'),
('María', 'López Díaz', '22.222.222-2', '1988-09-20', 'Av. Siempre Viva 742'),
('Pedro', 'Gómez Ruiz', '33.333.333-3', '1995-12-01', 'Pasaje Los Olmos 234'),
('Ana', 'Martínez Vega', '44.444.444-4', '1992-06-10', 'Camino Real 55'),
('Luis', 'Fuentes Herrera', '55.555.555-5', '1985-11-03', 'Diagonal Norte 88'),
('Carla', 'Reyes Silva', '66.666.666-6', '1998-02-14', 'Av. Los Aromos 456');

-- Contratos (asignar a distintas empresas)
INSERT INTO contratos (empleado_id, empresa_id, tipo, fecha_inicio, fecha_termino, sueldo_base, afp_id, salud_id, afc_id) VALUES
-- Empresa Alpha SPA
(1, 1, 'INDEFINIDO', '2023-03-01', null, 1200000, 1, 1, 1),
(2, 1, 'PLAZO_FIJO', '2024-05-01', '2025-12-01', 950000, 2, 2, 2),

-- Beta Servicios Ltda.
(3, 2, 'INDEFINIDO', '2022-01-15', null, 1300000, 2, 1, 1),
(4, 2, 'INDEFINIDO', '2024-09-01', null, 1100000, 1, 1, 1),

-- Gamma Consultores S.A.
(5, 3, 'PLAZO_FIJO', '2025-01-01', '2025-12-01', 800000, 1, 1, 2),
(6, 3, 'INDEFINIDO', '2023-07-20', null, 1500000, 2, 2, 1);