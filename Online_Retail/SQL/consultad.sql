SELECT 
    COUNT(*) FILTER (WHERE nm_fatura IS NULL) AS nm_fatura_null_count,
    COUNT(*) FILTER (WHERE cd_estoque IS NULL) AS cd_estoque_null_count,
    COUNT(*) FILTER (WHERE descricao IS NULL) AS descricao_null_count,
    COUNT(*) FILTER (WHERE quantidade IS NULL) AS quantidade_null_count,
    COUNT(*) FILTER (WHERE dt_fatura IS NULL) AS dt_fatura_null_count,
    COUNT(*) FILTER (WHERE vl_unitario IS NULL) AS vl_unitario_null_count,
    COUNT(*) FILTER (WHERE id_cliente IS NULL) AS id_cliente_null_count,
    COUNT(*) FILTER (WHERE pais IS NULL) AS pais_null_count
FROM 
    online_retail_refeito;


   
-- Verificar se tem algum registro com Cliente Nulo
SELECT 
	* 
FROM online_retail_refeito or2 
WHERE or2.id_cliente  IS NULL



SELECT 
	count(*) 
FROM online_retail_refeito or2 
WHERE 1 = 1
AND id_cliente = 0
-- AND id_cliente <= 0 ambos o mesmo resultado, ID CLIENTE ZERO TEM 135080 REGISTROS



SELECT 
	count(*) 
FROM online_retail_refeito or2 
WHERE 1 = 1
AND id_cliente != 0




-- Quantidade de registros com quantidade negativa
SELECT 
	quantidade ,
	count(*)  
FROM online_retail_refeito
WHERE quantidade <= 0
GROUP BY quantidade 
ORDER BY count(*) DESC



SELECT 
	quantidade ,
	count(*)  
FROM online_retail_refeito
WHERE quantidade = 0
GROUP BY quantidade 
ORDER BY count(*) DESC

--  Analiasando semelhanças entre cd_estoque e descricao
-- CONCLUSÃO: cada cd_estoque tem uma descricao, então, para descrições em branco, o ideal seria fazer um update caso tivesse casos com cd_estoque e sem descricao
-- É O CASO!
SELECT  
	DISTINCT cd_estoque ,
	descricao  
FROM online_retail_refeito orr 
ORDER BY descricao desc


SELECT count(*) FROM online_retail_refeito orr WHERE descricao IS null 




SELECT 
    *, 
    COUNT(*) FILTER (WHERE * IS NULL) AS null_count
FROM 
    online_retail_refeito
GROUP BY 
    *;

-- Provavel método duplicado
   SELECT 
   * 
   FROM online_retail_refeito orr 
   WHERE nm_fatura like '580877'
   AND id_cliente = 172500
   AND cd_estoque LIKE '84347'
   
   
   
   
   SELECT 
   *
   FROM online_retail_refeito WHERE descricao LIKE 'nan'
   
   SELECT * FROM online_retail_refeito WHERE cd_estoque LIKE '84251J'
 