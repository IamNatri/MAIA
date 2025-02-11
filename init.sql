CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    tipo VARCHAR(100),
    unidade VARCHAR(2),
    localizacao VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE leitura_sensores (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensores(id),
    valor NUMERIC,
    timestamp TIMESTAMP,
    sincronizado BOOLEAN DEFAULT FALSE
);

CREATE TABLE sincronizacao (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    status BOOLEAN,
    mensagem VARCHAR(255)
);

-- Inserção de dados
INSERT INTO sensores (nome, tipo, unidade, localizacao) 
VALUES ('SensorTemp', 'umidade', '°C', 'Lugar2');

INSERT INTO leitura_sensores (sensor_id, valor, timestamp)
VALUES (1, 23.5, '2025-01-28 10:00:00');
