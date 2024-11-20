DROP IF EXISTS TABLE logs_teste;

CREATE TABLE logs_teste (
    ID INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único para cada registro
    CLIENTE VARCHAR(255) NOT NULL,    -- Nome do cliente (subpasta)
    DOCUMENTO VARCHAR(255) NOT NULL,  -- Nome do arquivo .log
    DATA_HORA DATETIME,               -- Data e hora do log
    LOG TEXT                          -- Mensagem do log
);