# csv_preprocessor

CSVファイルの前処理を行う。

## csv_preprocessorコマンド


### カラムの排他(column-exclusive)

1行に同時に指定できないカラムを分離する。

```shell
poetry run csv_preprocessor column-exclusive -i test_data/header1/5x5.csv --header 1 --column-group [1,2] --column-group [3,4]
```

### カラムの移動(column-move)

カラムを移動する。

```shell
poetry run csv_preprocessor column-move -i test_data/header0/3x3.csv --from 2 --to 0
```

### カラムの選択(column-select)

指定したカラムの範囲を出力する。

```shell
poetry run csv_preprocessor column-select -i test_data/header0/3x3.csv --start 2 --end 3
```

### CSVファイルの種別を判定(csv-filetype)

CSVのヘッダ行からCSVファイルの種別を判定する。--header-dirディレクトリにヘッダ行だけを記述したファイルを格納する。FILESで指定したファイルのヘッダ行と一致する場合ファイル名をファイル種別として出力する

```shell
$ poetry run csv_preprocessor csv-filetype --header-dir test_data/header_type test_data/header1/2x2.csv test_data/header1/3x3.csv test_data/header1/5x5.csv test_data/header2/3x3.csv
test_data/header1/2x2.csv       ***unknown***
test_data/header1/3x3.csv       1x3
test_data/header1/5x5.csv       1x5
test_data/header2/3x3.csv       2x3
$ 
```

## tool_csvコマンド

テストデータを作成するコマンド

```shell
poetry run tool_csv make-csv --column-count 30 --row-count 1000 --type 2 --output tmp/1000x30.csv
```
