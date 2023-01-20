#! /usr/bin/env python3

import streamlit as st

####
st.snow()
st.markdown("""
## 目的
1. 過去3回の東京都区議会議員選挙における候補者への投票数と投票率(Election)。
2. 東京23区の区ごとの老年層、若年層の人口分布および15歳人口の増減推移(Population)。
3. 港区、目黒区、大田区、品川区、渋谷区、中央区（全世代のみ）、台東区における町丁目ごとの年齢層別人口分布(Ward Population)。

## 情報源
* e-Stat
* 国土交通省 GISホームページ

""")



# ## 情報源
# #
# #* [政治山](https://seijiyama.jp/)
# * [選挙ドットコム](https://go2senkyo.com/)
# ## 方法

# 1. [政治山](https://seijiyama.jp/) からChrome＋Table Capture拡張機能を使って表データをCSV（またはExcel）データとしてスクレープ。
# 2. 選挙概要は政治山では不十分なことがあるので、[選挙ドットコム](https://go2senkyo.com/) で補完。
# 3. jupyterフォルダにあるnotebook(lab)ファイルを使ってクレンジング。
# 4. 可視化は、各区ごとに当選者の得票数を過去3回の選挙を追って折れ線グラフ、表で示した。最上部には選挙の概要を示した。





















