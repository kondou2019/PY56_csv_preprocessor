# コマンドリファレンス(csv_preprocessor,column)

## サブコマンド(column)

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
poetry run csv_preprocessor column-exclusive -i test_data/header1/5x5.csv --column-group [1,2] --column-group [3,4]
```

### カラムの欠損値を置換(column-fill)

カラムの欠損値を置換(穴埋め)する。

```shell
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value x
poetry run csv_preprocessor column-fill -i test_data/header0/5x5_none.csv --column [1,3] --value x
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value-source ffill
# 先頭行が空白の場合は、xを穴埋め。以降は直前の行の値で穴埋め
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value-source ffill --value x 
# カラム0の値で穴埋め
poetry run csv_preprocessor column-fill -i test_data/header0/3x2_none.csv --column [1] --value-source column --value 0
```

--column-if  

書式  

```text
インデックス+比較演算子+値
```

比較演算子

| 演算子 | 意味       |
| ------ | ---------- |
| ==     |            |
| !=     |            |
| <      | 未サポート |
| >      | 未サポート |
| <=     | 未サポート |
| >=     | 未サポート |

カラム4が空で、カラム1が空ではない場合にカラム4にxをセットする

```shell
poetry run csv_preprocessor column-fill -i test_data/header0/5x5_none.csv --column [4] --value x --column-if 1!=''
```

### カラムをマージ(column-merge)

column-exclusiveで排他した行をマージして元にもどす。

```shell
poetry run csv_preprocessor column-merge -i tmp/5x5h1_ex.csv --column-key [0] --column-group [1,2] --column-group [3,4]
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
```

### カラムを置換する(column-replace)

カラムの値を置換する。

```shell
poetry run csv_preprocessor column-replace -i test_data/header0/3x3.csv --column [1] --regex 5 --repl A
# 正規表現
echo aaa@xxx.com,bbb@yyy.net,ccc@zzz.org | poetry run csv_preprocessor column-replace --column [1] --regex '[a-z]+@' --repl 'ABC@'
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
cat test_data/header1/5x5_sort.csv | poetry run csv_preprocessor csv-header-del --header 1 | poetry run csv_preprocessor column-sort --column-key [1,2]
```

数値順。--column-attr

```shell
cat test_data/header1/5x3_sort_int.csv | poetry run csv_preprocessor csv-header-del --header 1 | poetry run csv_preprocessor column-sort --column-key [1,2] --column-attr [int,str]
```
