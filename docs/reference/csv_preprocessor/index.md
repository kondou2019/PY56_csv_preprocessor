# コマンドリファレンス(csv_preprocessor)

## サブコマンド


| サブコマンド        | 機能                                                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------------------------------ |
| column-add          | [カラムを追加](column.md#カラムを追加column-add)                                                                   |
| column-del          | [カラムを削除](column.md#カラムを削除column-del)                                                                   |
| column-exclusive    | [カラムを排他。--column-groupで指定したカラムグループを別々の行に分離する](column.md#カラムを排他column-exclusive) |
| column-fill         | [カラムの欠損値を置換(穴埋め)](column.md#カラムの欠損値を置換穴埋めcolumn-fill)                                    |
| column-merge        | [カラムをマージ。column-exclusiveで排他した行をマージして元にもどす](column.md#カラムをマージcolumn-merge)         |
| column-move         | [カラムを移動](column.md#カラムを移動column-move)                                                                  |
| column-quote        | [カラムの値をクォートで囲む](column.md#カラムの値をクォートで囲むcolumn-quote)                                     |
| column-replace      | [カラムを置換する](column.md#カラムを置換するcolumn-replace)                                                       |
| column-select       | [カラムを選択](column.md#カラムを選択column-select)                                                                |
| column-sort         | [カラムでソート](column.md#カラムでソートcolumn-sort)                                                              |
| csv-filetype        | [CSVファイルの種別を判定](csv.md#csvファイルの種別を判定csv-filetype)                                              |
| csv-header-add      | [CSVファイルにヘッダを追加](csv.md#csvファイルにヘッダを追加csv-header-add)                                        |
| csv-header-change   | [CSVファイルのヘッダを変更](csv.md#csvファイルのヘッダを変更csv-header-change)                                     |
| csv-header-del      | [CSVファイルのヘッダを削除](csv.md#csvファイルのヘッダを削除csv-header-del)                                        |
| csv-report          | [CSVファイルの情報を表示](csv.md#csvファイルの情報を出力csv-report)                                                |
| custom-header-get   | [カスタムヘッダの取得](#カスタムヘッダの取得custom-header-get)                                                     |
| custom-header-line1 | [カスタムヘッダの取得](#カスタムヘッダを1行ヘッダに変換custom-header-line1)                                        |
| filter              | [フィルターモジュールによる加工](#フィルターモジュールによる加工filter)                                            |
| filter-list         | [フィルター一覧](#フィルター一覧filter-list)                                                                       |

### カスタムヘッダの取得(custom-header-get)

```shell
poetry run csv_preprocessor custom-header-get --separator == -i test_data/custom/data/1x3_a.csv
```

### カスタムヘッダを1行ヘッダに変換(custom-header-line1)

```shell
poetry run csv_preprocessor custom-header-line1 --separator == -i test_data/custom/data/1x3_a.csv
poetry run csv_preprocessor custom-header-line1 --separator == -i test_data/custom/data/1x8_b.csv
```

カラム名とインデックスの表示

```shell
poetry run csv_preprocessor custom-header-line1 --header 1 -i test_data/custom/data/1x8_b.csv | tr ',', '\n' | awk '{print NR-1, $0}'
```


### フィルターモジュールによる加工(filter)

複雑な加工を行う場合、pythonモジュールを作成する。作成したモジュールをフィルタとして実行する。  

```shell
poetry run csv_preprocessor filter --filter-name sample -i test_data/header1/3x3.csv
poetry run csv_preprocessor filter --filter-name sample --column [1] -i test_data/header1/3x3.csv
```

### フィルター一覧(filter-list)

フィルター一覧の出力  

```shell
poetry run csv_preprocessor filter-list
```

## カスタムフィルターの

[カスタムフィルターの作成](filter.md)
