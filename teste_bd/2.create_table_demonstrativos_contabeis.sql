CREATE TABLE IF NOT EXISTS demonstrativos_contabeis (
    id SERIAL PRIMARY KEY,
    data date, 
    registro_ans VARCHAR(20),
    conta_contabil VARCHAR(20),
    descricao VARCHAR(500),
    valor DECIMAL(15,2)
);