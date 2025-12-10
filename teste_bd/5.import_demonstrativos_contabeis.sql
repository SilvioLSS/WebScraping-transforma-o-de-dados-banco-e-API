-- 1. Criar tabela temporária com 6 colunas EXATAS
CREATE TEMP TABLE temp_demonstrativos (
    DATA TEXT,
    REG_ANS TEXT,
    CD_CONTA_CONTABIL TEXT,
    DESCRICAO TEXT,
    VL_SALDO_INICIAL TEXT,
    VL_SALDO_FINAL TEXT
);

-- 2. Importar todos os arquivos
COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\1T2024.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\2T2024.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\3T2024.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\4T2024.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\1T2025.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

COPY temp_demonstrativos FROM 'C:\TesteNivelamentoIC\teste_bd\dados\2T2025.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', ENCODING 'UTF-8');

-- 3. Criar tabela final
DROP TABLE IF EXISTS demonstrativos_contabeis;
CREATE TABLE demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    data DATE,
    registro_ans VARCHAR(20),
    cd_conta_contabil VARCHAR(20),
    descricao TEXT,
    vl_saldo_inicial DECIMAL(15,2),
    vl_saldo_final DECIMAL(15,2)  
);

-- 4. Inserir convertendo
INSERT INTO demonstrativos_contabeis 
(data, registro_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
SELECT 
    -- Converte data
    CASE 
        WHEN DATA ~ '^\d{4}-\d{2}-\d{2}$' THEN DATA::DATE
        WHEN DATA ~ '^\d{6}$' THEN TO_DATE(DATA || '01', 'YYYYMMDD')
        ELSE NULL 
    END,
    
    REG_ANS,
    CD_CONTA_CONTABIL,
    DESCRICAO,
    
    -- Converte números brasileiros para decimal
    NULLIF(REPLACE(REPLACE(VL_SALDO_INICIAL, '.', ''), ',', '.'), '')::DECIMAL(15,2),
    NULLIF(REPLACE(REPLACE(VL_SALDO_FINAL, '.', ''), ',', '.'), '')::DECIMAL(15,2)
FROM temp_demonstrativos;
