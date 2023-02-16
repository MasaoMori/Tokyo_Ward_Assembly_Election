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
datadir = d + '/data/'

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
# 世帯分布データ
#
households  = pd.read_csv(datadir + 'households.csv')

ward = ['品川区']

# ward=['港区','目黒区','大田区','品川区','渋谷区',
#       '中央区','台東区','千代田区','練馬区','世田谷区',
#       '北区','葛飾区','板橋区','江戸川区','墨田区','新宿区','文京区',
#       '中野区','杉並区','豊島区','江東区','足立区','荒川区']

w = st.sidebar.selectbox("区名", ward+'世帯数分布') # 区を選択

# 地図の色目を決める
cclr = st.sidebar.radio('地図の色',['赤','青','緑','黒','橙','紫'],horizontal=True)

# 選んだ市区のgeoデータ
gdf = gpd.read_file(geodir + w + '.geojson')

# Geoとデータのまーじ
result_tmp = pd.merge(households, gdf,
                      left_on=['区','町丁目名'],
                      right_on=['CITY_NAME','S_NAME'])

result = gpd.GeoDataFrame(result_tmp)

result_map = result.explore(column=result['世帯数'],
                            cmap=mapcolor[cclr],
                            tooltip=['町丁目名','世帯数'],
                            tiles='CartoDB positron')

st.subheader(w)
#    st.write('データ集計基準月（区発表）　'+refd[w])

    
st_folium(result_map, width='100%')

ag_res = result.sort_values('KEY_CODE')[['町丁目名','世帯数']]
AgGrid.AgGrid(ag_res, fit_columns_on_grid_load=True)
