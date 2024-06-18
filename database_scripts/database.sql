CREATE DATABASE IF NOT EXISTS banco_placas;

USE banco_placas;

CREATE TABLE IF NOT EXISTS placas_registradas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    descricao VARCHAR(255),
    data_hora DATETIME DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS registro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL,
    data_hora DATETIME DEFAULT NOW(),
    tipo VARCHAR(10)
);

-- Indexando
CREATE INDEX idx_placas_registradas_placa ON placas_registradas (placa);
