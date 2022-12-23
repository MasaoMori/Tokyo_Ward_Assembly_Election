#! /usr/bin/env python3

import streamlit as st
import pandas as pd
import plotly.express as px
import st_aggrid as AgGrid
import numpy as np
import os
import pathlib

cpath = os.getcwd()
ppath = str(pathlib.Path(cpath))

#####
parties = pd.read_csv(ppath + '/data/parties.csv')
ward_master = pd.read_csv(ppath + '/data/ward_master.csv')
summary = pd.read_csv(ppath + '/data/summary.csv')
data = pd.read_csv(ppath + '/data/election.csv',
                   dtype={'得票数':float,
                          '得票率%':float,
                          '年':str})
#####

st.set_page_config(layout="wide")
#### サイドバーでパラメータを決める
wardlist = ['中央', '台東', '品川', '目黒', '大田', '渋谷']
# yearlistは降順
yearlist = ('2019','2015','2011')
wardname = st.sidebar.selectbox("対象区名", wardlist)
year = st.sidebar.selectbox('年',yearlist)



pivot_columns = ['年','区名','氏名','得票数','得票率%','略称党名','自治体コード']

m = data[(data['当落']=='当') & (data['区名']==wardname)].loc[:,pivot_columns]

# m = pd.concat([tmp,tmp['氏名'] + '('+tmp['略称党名']+ ')'],axis=1).rename(columns={0:'候補者'})
# これはやめ

# 凡例の出現順序を決める
sorted_candidate = list(m[m['年']==year].sort_values('得票数',ascending=False)['氏名'])

#y_upper = np.ceil(max(m[m['年']==year]['得票数'])*1.3)
#y_lower = np.ceil(min(m[m['年']==year]['得票数'])*0.7)
# 縦軸の上限下限

import plotly.express as px
fig = px.line(
    m.sort_values('年'),
    x='年',
    y='得票数',
    text='得票数',
    color='氏名',
    category_orders={'氏名':sorted_candidate,
                     '年':['2011','2015','2019']},
    markers=True,
    height=1200,
    width=600
)

#fig.update_layout(xaxis=dict(range=(2010,2020),dtick=1),
#                  yaxis=dict(range=(y_lower,y_upper),dtick=1000))

mm = m.pivot(index=['氏名'],columns='年',values='得票数').sort_values(yearlist[-1],ascending=False).reset_index()


#
# Plot procedure

st.title(wardname+'区')
st.subheader('選挙概要')
AgGrid.AgGrid(summary[summary['区名']==wardname],fit_columns_on_grid_load=True,height=120)
st.subheader('得票数グラフ')
st.write("凡例は最新の選挙結果を降順に並べています。凡例の候補者名をダブルクリックすると、グラフ全体が消え、その候補者だけを表示できます。その状態で、他の候補者をシングルクリックすると、その候補者のグラフが出現します。")
st.plotly_chart(fig, use_container_width=True)
st.subheader('得票数表')
st.write("最新の選挙結果を降順に並べています。ヘッダの年をクリックすると、その年のデータで並び替えられます。空欄は実績がないことを意味します。")
AgGrid.AgGrid(mm,fit_columns_on_grid_load=True,height=600)
