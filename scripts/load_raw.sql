-- datalake配下のCSVをDuckDBのrawスキーマに取り込む（dbtの外で実行するロード処理）
-- 実行例: duckdb petstore_raw.duckdb < scripts/load_raw.sql
--   ※ dbtbook ディレクトリ直下から実行すること（datalake/ への相対パスを使用しているため）

CREATE SCHEMA IF NOT EXISTS raw;

-- ---------- マスタ ----------
CREATE OR REPLACE TABLE raw.customer_master AS
    SELECT * FROM read_csv_auto('datalake/masters/customer_master.csv', header = true);

CREATE OR REPLACE TABLE raw.species_master AS
    SELECT * FROM read_csv_auto('datalake/masters/species_master.csv', header = true);

CREATE OR REPLACE TABLE raw.goods_category_master AS
    SELECT * FROM read_csv_auto('datalake/masters/goods_category_master.csv', header = true);

CREATE OR REPLACE TABLE raw.product_master AS
    SELECT * FROM read_csv_auto('datalake/masters/product_master.csv', header = true);

-- ---------- トランザクション（日次ファイルをunionして取り込み） ----------
CREATE OR REPLACE TABLE raw.sales AS
    SELECT * FROM read_csv_auto('datalake/sales/sales_*.csv', header = true, union_by_name = true);

CREATE OR REPLACE TABLE raw.sales_detail AS
    SELECT * FROM read_csv_auto('datalake/sales_detail/sales_detail_*.csv', header = true, union_by_name = true);

-- ---------- 簡易確認 ----------
SELECT 'customer_master' AS table_name, COUNT(*) AS row_count FROM raw.customer_master
UNION ALL SELECT 'species_master', COUNT(*) FROM raw.species_master
UNION ALL SELECT 'goods_category_master', COUNT(*) FROM raw.goods_category_master
UNION ALL SELECT 'product_master', COUNT(*) FROM raw.product_master
UNION ALL SELECT 'sales', COUNT(*) FROM raw.sales
UNION ALL SELECT 'sales_detail', COUNT(*) FROM raw.sales_detail;
