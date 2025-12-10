-- Importar dados das operadoras (ajuste o caminho do arquivo)
COPY operadoras 
FROM 'C:\TesteNivelamentoIC\teste_bd\dados\operadoras.csv'
WITH (
    FORMAT CSV,
    HEADER TRUE,
    DELIMITER ';',
    ENCODING 'UTF-8'
);

