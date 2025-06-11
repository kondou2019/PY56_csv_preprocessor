# multi_value

## 使い方

複数値カラムの要素を変更。重複指定を排除

```shell
poetry run csv_preprocessor filter --filter-name multi_value -i test_data/header1/3x3.csv --filter-option "--regex ^a$ --repl x"
```
