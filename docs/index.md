# csv_preprocessor

## コマンド


| コマンド                                          | 機能                           |
| ------------------------------------------------- | ------------------------------ |
| [csv_preprocessor](reference/csv_preprocessor.md) | CSVファイルの前処理を行う。    |
| [tool_csv](reference/tool_csv.md)                 | テストデータを作成するコマンド |

## CSVファイルの加工手順

CSVファイルのヘッダがない状態でcolumn系コマンドで加工する。  
ヘッダ削除->加工->ヘッダ追加  

## カラムの階層構造

カラムに複数のデータを記述するとき、行を分割して記述したい場合がある。column-exclusiveを使うことで行を分割することができる。
更にカラム階層構造になっている場合は、column-exclusiveを複数回実行することで更に分割することができる。

マージ
column-mergeをつかうことでcolumn-exclusiveで分割した行を元に戻すことができる。
階層構造になっている場合は、column-exclusiveと逆の手順で実行することで元に戻すことができる。

## 実行例

### カラムを追加

- ヘッダを削除
- カラムを追加
- 追加したカラムに'x'をセット
- 新しいヘッダを追加

```shell
cat test_data/header1/3x3.csv | \
poetry run csv_preprocessor csv-header-del --header 1 | \
poetry run csv_preprocessor column-add --column [-1] | \
poetry run csv_preprocessor column-fill --column [3] --value x | \
poetry run csv_preprocessor csv-header-add --input-header test_data/csv_info/1x4_header.csv
```

### 特定のファイルの表示

ディレクトリ下のsample.csvのファイルからヘッダを削除し3カラム目を出力する

```shell
find sample/csv -type f -name "sample.csv" -print0 | \
xargs -0 -i bash -c '\
cat {} \ 
poetry run csv_preprocessor csv-headr-del --header 2 | \
poetry run csv_preprocessor column-select --column [2]
```
