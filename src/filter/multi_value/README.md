# multi_value

## 使い方

複数値カラムの要素を変更。重複指定を排除


| オプション   | 必須 | 説明                                   | 例  |
| ------------ | ---- | -------------------------------------- | --- |
| regex        | 必須 | 置換文字列                             | ^a$ |
| repl         | 必須 | 置換後文字列                           | x   |
| uniq         | -    | 重複排除。置換後に同一の値の場合に削除 |     |
| empty_remove | -    | 空文字に変換した場合、削除             |     |


```shell
poetry run csv_preprocessor filter --filter-name multi_value -i test_data/header1/3x3.csv --filter-option "--regex ^a$ --repl x"
```
