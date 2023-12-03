# csv_preprocessor

CSVファイルの前処理を行う。

## csv_preprocessorサブコマンド

### カラムの排他(column-exclusive)

1行に同時に指定できないカラムを分離する。

```shell
poetry run csv_preprocessor column-exclusive -i test_data/header1/5x5.csv --header 1 --column-group [1,2] --column-group [3,4]
```

### カラムのマージ(column-merge)

column-exclusiveで排他した行をマージして元にもどす。

```shell
poetry run csv_preprocessor column-merge -i tmp/5x5h1_ex.csv --header 1 --column-key [0] --column-group [1,2] --column-group [3,4]
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

CSVのヘッダ行からCSVファイルの種別を判定する。--csv-info-dirディレクトリにヘッダ行だけを記述したファイルを格納する。FILESで指定したファイルのヘッダ行と一致する場合ファイル名をファイル種別として出力する。

```shell
$ poetry run csv_preprocessor csv-filetype --csv-info-dir test_data/csv_info test_data/header1/2x2.csv test_data/header1/3x3.csv test_data/header1/5x5.csv test_data/header2/3x3.csv
test_data/header1/2x2.csv       ***unknown***
test_data/header1/3x3.csv       1x3
test_data/header1/5x5.csv       1x5
test_data/header2/3x3.csv       2x3
$ 
```

### CSVファイルのヘッダを変更(csv-header-change)

CSVファイルのヘッダを変更する。

```shell
poetry run csv_preprocessor csv-header-change --input test_data/header1/3x3.csv --input-header test_data/csv_info/1x3_header.csv --output-header test_data/csv_info/2x3_header.csv
```

### CSVファイルの情報を出力(csv-report)

CSVファイルの情報をJSON形式で出力する。

```shell
poetry run csv_preprocessor csv-report --csv-info-dir test_data/csv_info test_data/header1/2x2.csv test_data/header1/3x3.csv test_data/header1/5x5.csv test_data/header2/3x3.csv
```

## カラムの階層構造

カラムに複数のデータを記述するとき、行を分割して記述したい場合がある。column-exclusiveを使うことで行を分割することができる。
更にカラム階層構造になっている場合は、column-exclusiveを複数回実行することで更に分割することができる。

マージ
column-mergeをつかうことでcolumn-exclusiveで分割した行を元に戻すことができる。
階層構造になっている場合は、column-exclusiveと逆の手順で実行することで元に戻すことができる。

## tool_csvコマンド

テストデータを作成するコマンド

```shell
poetry run tool_csv make-csv --column-count 30 --row-count 1000 --type 2 --output tmp/1000x30.csv
```
