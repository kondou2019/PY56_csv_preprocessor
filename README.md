# csv_preprocessor

CSVファイルの前処理を行う。

## csv_preprocessorサブコマンド

### カラムを追加(column-add)

カラムを追加する。

```shell
poetry run csv_preprocessor column-add -i test_data/header0/3x3.csv --column [0]
poetry run csv_preprocessor column-add -i test_data/header0/3x3.csv --column [0,1]
poetry run csv_preprocessor column-add -i test_data/header0/3x3.csv --column [0] --column-count 3
# 最後に追加
poetry run csv_preprocessor column-add -i test_data/header0/3x3.csv --column [-1]
```

### カラムを削除(column-del)

カラムを削除する。

```shell
poetry run csv_preprocessor column-del -i test_data/header0/3x3.csv --column [0,1]
```

### カラムを排他(column-exclusive)

1行に同時に指定できないカラムを分離する。

```shell
poetry run csv_preprocessor column-exclusive -i test_data/header1/5x5.csv --header 1 --column-group [1,2] --column-group [3,4]
```

### カラムの欠損値を置換(column-fill)

カラムの欠損値を置換(穴埋め)する。

```shell
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value x
poetry run csv_preprocessor column-fill -i test_data/header0/5x5_none.csv --column [1,3] --value x
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --ffill
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value x --ffill
# ヘッダ行をスキップ
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value x --header 1

# カラム4が空で、カラム1が空ではない場合にカラム4にxをセットする
poetry run csv_preprocessor column-fill -i test_data/header0/5x5_none.csv --column [4] --value x --row-if 1!=''
```

### カラムをマージ(column-merge)

column-exclusiveで排他した行をマージして元にもどす。

```shell
poetry run csv_preprocessor column-merge -i tmp/5x5h1_ex.csv --header 1 --column-key [0] --column-group [1,2] --column-group [3,4]
```

### カラムを移動(column-move)

カラムを移動する。  
--fromで指定したインデックスのカラムを取出してから--toで指定したインデックスに追加します。
そのため--toで指定するインデックスは、--fromで指定したカラムが無くなった後のインデックスを指定します。

```shell
poetry run csv_preprocessor column-move -i test_data/header0/3x3.csv --from [2] --to [0]
# 先頭に移動する。順番は--fromの順番になる
 poetry run csv_preprocessor column-move -i test_data/header0/5x5.csv --from [2,3] --to [0,0]
poetry run csv_preprocessor column-move -i test_data/header0/5x5.csv --from [3,2] --to [0,0]
```

### カラムの値をクォートで囲む(column-quote)

カラムの値をクォートで囲む。

```shell
poetry run csv_preprocessor column-quote -i test_data/header0/3x3.csv --column [0]
poetry run csv_preprocessor column-quote -i test_data/header0/3x3.csv --header 1 --column [0]
```

### カラムを選択(column-select)

指定したカラムを出力する。
カラムの順番を変更することにも使用できる。

```shell
poetry run csv_preprocessor column-select -i test_data/header0/3x3.csv --column [1]
poetry run csv_preprocessor column-select -i test_data/header0/3x3.csv --column [1,0,2]
```

### カラムでソート(column-sort)

CSVファイルをソートする。

```shell
poetry run csv_preprocessor column-sort -i test_data/header1/5x5_sort.csv --column-key [1,2] --header 1
```

数値順。--column-attr

```shell
poetry run csv_preprocessor column-sort -i test_data/header1/5x3_sort_int.csv --header 1 --column-key [1,2] --column-attr [int,str]
```

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
poetry run csv_preprocessor csv-header-add -i test_data/header0/3x3.csv --add-header test_data/csv_info/1x3_header.csv
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
