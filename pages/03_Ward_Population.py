import pandas as pd
import geopandas as gpd
import folium
import matplotlib
import mapclassify
import numpy as np
import os
import streamlit as st
import st_aggrid as AgGrid
from streamlit_folium import st_folium


### 各種定数の設定
#
# ファイルのありか
#
d = os.getcwd()
geodir = d + '/geoshape/' 

#
# 世代
#
fiveband = ['0~4歳', '5~9歳', '10~14歳', '15~19歳', '20~24歳', '25~29歳', '30~34歳',
 '35~39歳', '40~44歳', '45~49歳', '50~54歳', '55~59歳', '60~64歳', '65~69歳',
 '70~74歳', '75~79歳', '80~84歳', '85~89歳', '90~94歳', '95~99歳', '100~104歳',
 '105~109歳', '110~114歳', '115~119歳', '120~124歳', '125~129歳']#, '130歳以上']

#
# 地図の色目
#
mapcolor = {'赤':'Reds',
         '青':'Blues',
         '緑':'Greens',
         '黒':'Greys',
         '橙':'Oranges',
         '紫':'Purples'
         }

#
# 人口分布データ・中央区だけ全世代のみ
#
final = pd.read_csv(d+'/data/Ward_Age/final_data.csv')
chu_final = pd.read_csv(d+'/data/Ward_Age/final_chu_data.csv')
rf = pd.read_csv(d+'/data/Ward_Age/Ward_data_reference_date.csv')

refd = dict(zip(list(rf['区名']),list(rf['データ基準日'])))

ward=['港区','目黒区','大田区','品川区','渋谷区','中央区','台東区','千代田区','練馬区','世田谷区']

w = st.sidebar.selectbox("区名", ward) # 区を選択

if w == '中央区':
    # 中央区は全世代のデータしかないので、fb = ['全世代']に設定するためallを真に
    all = True
else:
    all = st.sidebar.checkbox('全世代の総和で可視化') # 全世代で見る場合のチェックボックス


if all:
    # 全世代チェックボックスを選ぶと、マルチセレクトボックスが表示されない
    fb = ['全世代'] 
else:
    # 世代を複数可選択
    fb = st.sidebar.multiselect('世代', fiveband, ['15~19歳', '20~24歳'])
    st.sidebar.write('世代は複数選べます。')


# 地図の色目を決める
cclr = st.sidebar.radio('地図の色',['赤','青','緑','黒','橙','紫'],horizontal=True)

if fb == []:
    # 世代が一つも選ばれなかったら、警告
    st.warning('少なくとも1つの世代を選んでください。')    
else:
    if w == '中央区':
        # 中央区はすでに全世代データはでているのでgroupbyはしないでqoqに代入
        pop = chu_final
    else:
        # 中央区以外は区名で抽出
        pop = final[final['区']==w]
        qoq = pd.DataFrame()

    if fb == ['全世代']:
        gen = '全世代'
        qoq = pop
    else:
        gen = ','.join(fb)
        for g in fb:
            qoq = pd.concat([qoq, pop[pop['世代']==g]])

    qoq = qoq.groupby(['区','町丁目名'])['人口'].sum().reset_index()

    gdf = gpd.read_file(geodir + w + '.geojson')
    gdf = gdf[gdf['HCODE']==8101]

    result = pd.merge(qoq, gdf, left_on=['区','町丁目名'], right_on=['CITY_NAME','S_NAME'])# , how='right')
    result['世代'] = gen

    result = gpd.GeoDataFrame(result)

    result_map = result.explore(column=result['人口'],
                                cmap=mapcolor[cclr],
                                tooltip=['町丁目名','世代','人口'],
                                tiles='CartoDB positron')

    st.subheader(w)
    st.write('データ集計基準月（区発表）　'+refd[w])

    for f in fb:
        st.write(f)

    st_folium(result_map, width='100%')

    ag_res = result.sort_values('KEY_CODE')[['町丁目名','世代','人口']]
    AgGrid.AgGrid(ag_res, fit_columns_on_grid_load=True)
