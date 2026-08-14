-- sources配下のCSVを petstore/dev.duckdb の petstore_raw スキーマにテーブルとして取り込む。
-- dbt からは source() 経由でこの petstore_raw スキーマの実テーブルを参照する想定。
--
-- 本来の取り込みは Airflow の DAG（airflow/dags/load_petstore_raw.py）が担う。
-- このスクリプトは Airflow を起動せずに手元で同じ取り込みを行いたい場合の手動実行用。
--
-- 実行例（dbtbook ディレクトリ直下から実行すること。CSVへの相対パスが
-- sources/... 基準のため）:
--   duckdb petstore/dev.duckdb < scripts/load_petstore_raw.sql

CREATE SCHEMA IF NOT EXISTS petstore_raw;

-- ---------- マスタ ----------
CREATE OR REPLACE TABLE petstore_raw.species_master AS
    SELECT * FROM read_csv_auto('sources/masters/species_master.csv', header = true);

CREATE OR REPLACE TABLE petstore_raw.goods_category_master AS
    SELECT * FROM read_csv_auto('sources/masters/goods_category_master.csv', header = true);

CREATE OR REPLACE TABLE petstore_raw.product_master AS
    SELECT * FROM read_csv_auto('sources/masters/product_master.csv', header = true);

-- ---------- トランザクション ----------
CREATE OR REPLACE TABLE petstore_raw.customer AS
    SELECT * FROM read_csv_auto('sources/transactions/customer.csv', header = true);

-- 日次ファイルをunionして取り込み
CREATE OR REPLACE TABLE petstore_raw.sales AS
    SELECT * FROM read_csv_auto(
        'sources/transactions/sales/sales_*.csv',
        header = true, union_by_name = true
    );

CREATE OR REPLACE TABLE petstore_raw.sales_detail AS
    SELECT * FROM read_csv_auto(
        'sources/transactions/sales_detail/sales_detail_*.csv',
        header = true, union_by_name = true
    );

-- ---------- 簡易確認 ----------
SELECT 'customer' AS table_name, COUNT(*) AS row_count FROM petstore_raw.customer
UNION ALL SELECT 'species_master', COUNT(*) FROM petstore_raw.species_master
UNION ALL SELECT 'goods_category_master', COUNT(*) FROM petstore_raw.goods_category_master
UNION ALL SELECT 'product_master', COUNT(*) FROM petstore_raw.product_master
UNION ALL SELECT 'sales', COUNT(*) FROM petstore_raw.sales
UNION ALL SELECT 'sales_detail', COUNT(*) FROM petstore_raw.sales_detail;
