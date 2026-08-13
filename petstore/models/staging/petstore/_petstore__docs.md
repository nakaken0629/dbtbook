{% docs petstore_source %}
オンラインペットショップの基幹データに存在する以下のソースを扱います。

- 顧客
- 商品マスタ
- 売上

scripts/create_petstore_raw_views.sql により sources/ 配下のCSVをpetstore_raw スキーマのビューとして dev.duckdb 上に作成したもの。
DuckDBのread_csv関数を使っているため**リアルタイムで**CSVの内容がソースに反映されます。
{% enddocs %}
