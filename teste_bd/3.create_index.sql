-- Índices para melhor performance nas consultas
CREATE INDEX idx_dc_registro_ans ON demonstrativos_contabeis(registro_ans);
CREATE INDEX idx_dc_data ON demonstrativos_contabeis(data);
CREATE INDEX idx_dc_conta ON demonstrativos_contabeis(conta_contabil);
CREATE INDEX idx_ops_registro ON operadoras_saude(registro_ans);