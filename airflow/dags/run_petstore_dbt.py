"""petstore の dbt プロジェクトを実行する DAG。

Airflow コンテナ自体に dbt-duckdb をインストールし（airflow/Dockerfile で
apache/airflow イメージを拡張してビルド）、petstore/ をマウントした
airflow-worker コンテナ内で dbt CLI を直接実行する。load_petstore_raw DAG
の完了後にトリガーされる想定。
"""
from __future__ import annotations

from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator

PETSTORE_DIR = "/opt/airflow/petstore"


@dag(
    dag_id="run_petstore_dbt",
    description="petstoreプロジェクトのdbtを実行する",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["petstore", "dbt"],
)
def run_petstore_dbt():
    BashOperator(
        task_id="dbt_build",
        # dbt-duckdb は profiles.yml の path（dev.duckdb）を --project-dir ではなく
        # 実行時のカレントディレクトリ基準で解決するため、先に petstore/ へ cd する。
        bash_command=f"cd {PETSTORE_DIR} && dbt build --profiles-dir {PETSTORE_DIR}",
    )


dag = run_petstore_dbt()
