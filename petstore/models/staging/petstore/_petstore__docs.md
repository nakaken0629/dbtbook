{% docs petstore_source %}
オンラインペットショップの基幹データに存在する以下のソースを扱います。

- 顧客
- 商品マスタ
- 売上

Airflow のDAG（airflow/dags/load_petstore_raw.py）により sources/ 配下のCSVを読み込み、
petstore_raw スキーマのテーブルとして dev.duckdb 上に作成したもの。
DAGを実行（またはAirflowを使わない場合は scripts/load_petstore_raw.sql を手動実行）するたびに
テーブルが最新のCSVの内容で洗い替えされます。
{% enddocs %}
