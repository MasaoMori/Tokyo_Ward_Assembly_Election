import pandas as pd
import geopandas as gpd
import folium
import matplotlib
import mapclassify
import numpy as np
import os
import streamlit as st
from streamlit_folium import st_folium

d = os.getcwd()
geodir = d + '/geoshape/'
fiveband = ['0~4歳', '5~9歳', '10~14歳', '15~19歳', '20~24歳', '25~29歳', '30~34歳',
 '35~39歳', '40~44歳', '45~49歳', '50~54歳', '55~59歳', '60~64歳', '65~69歳',
 '70~74歳', '75~79歳', '80~84歳', '85~89歳', '90~94歳', '95~99歳', '100~104歳',
 '105~109歳', '110~114歳', '115~119歳', '120~124歳', '125~129歳']#, '130歳以上']
final = pd.read_csv(d+'/data/Ward_Age/final_data.csv')

ward=['港区','目黒区','大田区','品川区','渋谷区']

w = st.sidebar.selectbox("区名", ward)
f = st.sidebar.selectbox('世代', fiveband)

gdf = gpd.read_file(geodir + w + '.geojson')
gdf = gdf[gdf['HCODE']==8101]
kgdf = pd.merge(final, gdf, left_on=['区','町丁目名'], right_on=['CITY_NAME','S_NAME'], how='left')
kgdf = kgdf[kgdf['区']==w]
kgdf = kgdf[kgdf['世代']==f]
tmp_kgdf = gpd.GeoDataFrame(kgdf)

m = tmp_kgdf.explore(column=tmp_kgdf['人口'],cmap='Reds',tooltip=['町丁目名','人口'],tiles='CartoDB positron')

st.subheader(w+f)
st_data = st_folium(m)

