DROP VIEW IF EXISTS view_dcalendario;
CREATE VIEW view_dcalendario
AS

SELECT 
    dcalendario.*,
    RIGHT(TO_CHAR(data_mes_final, 'YYYY-MM-DD'), 2) AS dias_mes
FROM dcalendario



