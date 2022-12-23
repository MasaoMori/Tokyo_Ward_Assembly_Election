# 東京区議会議員選挙分析


## ファイル構成

+ README.md このファイル
+ 00_twea.py アプリケーショントップ
+ pages 分析アプリのフォルダ
+ jupyter クレンジングのためのjupyter labファイル
+ data 分析データ

## 目的
過去3回の東京都区議会議員選挙における候補者への投票数を表示する。

## 情報源

* [政治山](https://seijiyama.jp/)
* [選挙ドットコム](https://go2senkyo.com/)


## 方法

1. [政治山](https://seijiyama.jp/) からChrome＋Table Capture拡張機能を使って表データをCSV（またはExcel）データとしてスクレープ。
2. 選挙概要は政治山では不十分なことがあるので、[選挙ドットコム](https://go2senkyo.com/) で補完。
3. jupyterフォルダにあるnotebook(lab)ファイルを使ってクレンジング。
4. 可視化は、各区ごとに当選者の得票数を過去3回の選挙を追って折れ線グラフ、表で示した。最上部には選挙の概要を示した。


