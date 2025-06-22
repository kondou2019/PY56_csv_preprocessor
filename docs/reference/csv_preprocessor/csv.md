# コマンドリファレンス(csv_preprocessor,csv)

## サブコマンド(csv)

### CSVファイルの種別を判定(csv-filetype)

CSVのヘッダ行からCSVファイルの種別を判定する。--csv-info-dirディレクトリにヘッダ行だけを記述したファイルを格納する。FILESで指定したファイルのヘッダ行と一致する場合ファイル名をファイル種別として出力する。  
CSVヘッダ情報ファイルは、ファイルの名のサフィックスが*_header.csvであること。

```shell
$ poetry run csv_preprocessor csv-filetype --csv-info-dir test_data/csv_info test_data/header1/2x2.csv test_data/header1/3x3.csv test_data/header1/5x5.csv test_data/header2/3x3.csv
test_data/header1/2x2.csv       ***unknown***
test_data/header1/3x3.csv       1x3
test_data/header1/5x5.csv       1x5
test_data/header2/3x3.csv       2x3
$ 
```

### CSVファイルにヘッダを追加(csv-header-add)

CSVファイルにヘッダを追加する。

```shell
poetry run csv_preprocessor csv-header-add -i test_data/header0/3x3.csv --input-header test_data/csv_info/1x3_header.csv
```

### CSVファイルのヘッダを変更(csv-header-change)

CSVファイルのヘッダを変更する。

```shell
poetry run csv_preprocessor csv-header-change --input test_data/header1/3x3.csv --input-header test_data/csv_info/1x3_header.csv --output-header test_data/csv_info/2x3_header.csv
```

### CSVファイルのヘッダを削除(csv-header-del)

CSVファイルのヘッダを削除する。

```shell
poetry run csv_preprocessor csv-header-del -i test_data/header1/3x3.csv --header 1
# ヘッダファイル指定
poetry run csv_preprocessor csv-header-del -i test_data/header1/3x3.csv --input-header test_data/csv_info/1x3_header.csv
```

### CSVファイルの情報を出力(csv-report)

CSVファイルの情報をJSON形式で出力する。

```shell
poetry run csv_preprocessor csv-report --csv-info-dir test_data/csv_info test_data/header1/2x2.csv test_data/header1/3x3.csv test_data/header1/5x5.csv test_data/header2/3x3.csv
```

