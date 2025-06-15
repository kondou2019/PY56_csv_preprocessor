# row_del

## 使い方

行削除

| オプション | 必須 | 説明     | 例    |
| ---------- | ---- | -------- | ----- |
| column-if  | 必須 | 削除条件 | 1!='' |


```shell
poetry run csv_preprocessor filter --filter-name row_del -i test_data/header0/3x3.csv --filter-option "--column_if 0=='4'"
```
