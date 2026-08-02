-- sources配下のCSVをSELECTで直接参照するビューを petstore_raw スキーマに作成する。
-- petstore/dev.duckdb（dbtプロジェクトのdevターゲット）に対して実行し、
-- dbt からは source() 経由でこの petstore_raw スキーマのビューを参照する想定。
--
-- 実行例（petstore/ ディレクトリの中から実行すること）:
--   cd petstore
--   duckdb dev.duckdb < ../scripts/create_petstore_raw_views.sql
--
-- ※ DuckDBのビューは read_csv_auto の相対パスを「作成時」ではなく
--    「クエリ実行時のカレントディレクトリ」を基準に解決する。
--    そのため、ここでは dev.duckdb と同じ場所（petstore/）を基準にした
--    相対パス（../sources/...）にしている。dbt もプロジェクトディレクトリ
--    （petstore/）内から実行するため、この前提と自然に一致する。

CREATE SCHEMA IF NOT EXISTS petstore_raw;

-- ---------- マスタ ----------
CREATE OR REPLACE VIEW petstore_raw.species_master AS
    SELECT * FROM read_csv_auto('../sources/masters/species_master.csv', header = true);

CREATE OR REPLACE VIEW petstore_raw.goods_category_master AS
    SELECT * FROM read_csv_auto('../sources/masters/goods_category_master.csv', header = true);

CREATE OR REPLACE VIEW petstore_raw.product_master AS
    SELECT * FROM read_csv_auto('../sources/masters/product_master.csv', header = true);

-- ---------- トランザクション ----------
CREATE OR REPLACE VIEW petstore_raw.customer AS
    SELECT * FROM read_csv_auto('../sources/transactions/customer.csv', header = true);

-- 日次ファイルをunionして参照
CREATE OR REPLACE VIEW petstore_raw.sales AS
    SELECT * FROM read_csv_auto(
        '../sources/transactions/sales/sales_*.csv',
        header = true, union_by_name = true
    );

CREATE OR REPLACE VIEW petstore_raw.sales_detail AS
    SELECT * FROM read_csv_auto(
        '../sources/transactions/sales_detail/sales_detail_*.csv',
        header = true, union_by_name = true
    );

-- ---------- 簡易確認 ----------
SELECT 'customer' AS view_name, COUNT(*) AS row_count FROM petstore_raw.customer
UNION ALL SELECT 'species_master', COUNT(*) FROM petstore_raw.species_master
UNION ALL SELECT 'goods_category_master', COUNT(*) FROM petstore_raw.goods_category_master
UNION ALL SELECT 'product_master', COUNT(*) FROM petstore_raw.product_master
UNION ALL SELECT 'sales', COUNT(*) FROM petstore_raw.sales
UNION ALL SELECT 'sales_detail', COUNT(*) FROM petstore_raw.sales_detail;
