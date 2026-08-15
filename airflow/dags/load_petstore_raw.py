"""sources/ 配下のCSVを DuckDB(petstore/dev.duckdb)の petstore_raw スキーマへ
テーブルとして取り込む DAG。

これまで dbt からは petstore_raw スキーマの CSV を直接参照するビューを
経由していたが、このDAGが CSV の内容を実テーブルへロードし、
dbt の source() は petstore_raw スキーマの実テーブルを参照する。

各テーブルのロードタスクは互いに依存しないため、DAG上は並列実行可能な形にしている。
ただし DuckDB はファイルへの書き込みを同時に1接続しか許可しないため、
Airflow の Pool（duckdb_writer, スロット数1）で実際の同時実行数を1に絞り、
書き込みが競合しないようにしている。
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import duckdb
from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

SOURCES_DIR = Path("/opt/airflow/sources")
DUCKDB_PATH = Path("/opt/airflow/petstore/dev.duckdb")
SCHEMA = "petstore_raw"


def _load_table(table_name: str, csv_glob: str) -> None:
    csv_path = SOURCES_DIR / csv_glob
    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
        con.execute(
            f"""
            CREATE OR REPLACE TABLE {SCHEMA}.{table_name} AS
            SELECT * FROM read_csv_auto(?, header = true, union_by_name = true)
            """,
            [str(csv_path)],
        )
        row_count = con.execute(f"SELECT COUNT(*) FROM {SCHEMA}.{table_name}").fetchone()[0]
    finally:
        con.close()
    print(f"{table_name}: loaded {row_count} rows from {csv_path}")


@dag(
    dag_id="load_petstore_raw",
    description="sources配下のCSVをDuckDB(petstore_raw)の実テーブルへロードする",
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["petstore", "duckdb"],
)
def load_petstore_raw():
    @task(pool="duckdb_writer")
    def load_species_master():
        _load_table("species_master", "masters/species_master.csv")

    @task(pool="duckdb_writer")
    def load_goods_category_master():
        _load_table("goods_category_master", "masters/goods_category_master.csv")

    @task(pool="duckdb_writer")
    def load_product_master():
        _load_table("product_master", "masters/product_master.csv")

    @task(pool="duckdb_writer")
    def load_customer():
        _load_table("customer", "transactions/customer.csv")

    @task(pool="duckdb_writer")
    def load_sales():
        _load_table("sales", "transactions/sales/sales_*.csv")

    @task(pool="duckdb_writer")
    def load_sales_detail():
        _load_table("sales_detail", "transactions/sales_detail/sales_detail_*.csv")

    trigger_dbt = TriggerDagRunOperator(
        task_id="trigger_run_petstore_dbt",
        trigger_dag_id="run_petstore_dbt",
    )

    load_tasks = [
        load_species_master(),
        load_goods_category_master(),
        load_product_master(),
        load_customer(),
        load_sales(),
        load_sales_detail(),
    ]

    load_tasks >> trigger_dbt


dag = load_petstore_raw()

