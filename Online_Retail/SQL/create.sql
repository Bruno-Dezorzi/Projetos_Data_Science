DROP TABLE IF EXISTS online_retail;

CREATE TABLE online_retail (
id serial PRIMARY KEY,
InvoiceNo VARCHAR(225),
StockCode	VARCHAR(225),
Description	VARCHAR(225),
Quantity	VARCHAR(225),
InvoiceDate VARCHAR(225),
UnitPrice	VARCHAR(225),
CustomerID	VARCHAR(225),
Country VARCHAR(225)
);

--  script python -> IMPORTACAO

DROP TABLE IF EXISTS online_retail_refeito;

CREATE TABLE online_retail_refeito (
id serial PRIMARY KEY,
nm_fatura VARCHAR(225),
cd_estoque	VARCHAR(225),
descricao VARCHAR(225),
quantidade	INTEGER,
dt_fatura  TIMESTAMP,
vl_unitario	FLOAT,
id_cliente	integer,
pais VARCHAR(225)
);

INSERT INTO online_retail_refeito (
    nm_fatura,
    cd_estoque,
    descricao,
    quantidade,
    dt_fatura,
    vl_unitario,
    id_cliente,
    pais
)
SELECT	
    invoiceno, 
    stockcode, 
    description, 
    CAST(quantity AS integer), 
    CAST(invoicedate AS timestamp), 
    CAST(unitprice AS float), 
    CAST(
        CASE 
            WHEN customerid = 'nan' THEN '0' -- Substitui "nan" por 0
            ELSE REPLACE(customerid, '.', '') -- Remove pontos
        END AS integer
    ),
    country
FROM 
    public.online_retail
;

-- Ajustando casos de NaN em descrições que não possuem dados validos


UPDATE online_retail_refeito t1
SET descricao = t2.descricao
FROM (
    SELECT 
        cd_estoque,
        descricao
    FROM online_retail_refeito
    WHERE descricao NOT LIKE 'nan'
) AS t2
WHERE t1.cd_estoque = t2.cd_estoque
  AND t1.descricao LIKE 'nan';



