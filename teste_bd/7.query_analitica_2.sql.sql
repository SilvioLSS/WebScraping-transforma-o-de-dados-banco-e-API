SELECT 
    o.razao_social,
    o.nome_fantasia,
    SUM(d.vl_saldo_final) AS total_despesas
FROM demonstrativos_contabeis d
JOIN operadoras o
    ON d.registro_ans = o.registro_ans
WHERE d.descricao ILIKE '%EVENTOS%'
  AND d.data >= DATE_TRUNC('year', '2025-04-01'::DATE) - INTERVAL '1 year'  
  AND d.data <= '2025-04-01'::DATE 
GROUP BY o.razao_social, o.nome_fantasia
ORDER BY total_despesas DESC
LIMIT 10;