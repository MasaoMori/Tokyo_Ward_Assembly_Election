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
#ward_master = pd.read_csv(ppath + '/data/ward_master.csv')
tkcode = pd.read_csv(ppath + '/data/tkcode.csv')
summary = pd.read_csv(ppath + '/data/summary.csv')
data = pd.read_csv(ppath + '/data/election.csv',
                   dtype={'得票数':float,
                          '得票率%':float,
                          '年':str})
#####

st.set_page_config(layout="wide")
#st.snow()
#### サイドバーでパラメータを決める
wardlist = list(tkcode[(131000 < tkcode['自治体コード']) & (tkcode['自治体コード'] < 132000)]['区名'])
wardlist = list(map((lambda x: x.replace('区','')),wardlist))

wardname = st.sidebar.selectbox("対象区名", wardlist)
obj_value = st.sidebar.radio('実数か割合を選んでください',('得票数','得票率%'))

# year = st.sidebar.selectbox('年',yearlist)
sum_tmp = summary[summary['区名']==wardname]
yearlist = list(map((lambda x: str(x)),list(sum_tmp.sort_values('年', ascending=False)['年'])))

year = yearlist[0]


pivot_columns = ['年','区名','氏名','得票数','得票率%','略称党名','自治体コード']

m = data[(data['当落']=='当') & (data['区名']==wardname)].loc[:,pivot_columns]


# 凡例の出現順序を決める
sorted_candidate = list(m[m['年']==year].sort_values(obj_value, ascending=False)['氏名'])

#y_upper = np.ceil(max(m[m['年']==year]['得票数'])*1.3)
#y_lower = np.ceil(min(m[m['年']==year]['得票数'])*0.7)
# 縦軸の上限下限


import plotly.express as px
fig = px.line(
    m.sort_values('年'),
    x='年',
    y=obj_value,
    text=obj_value,
    color='氏名',
    category_orders={'氏名':sorted_candidate,
                     '年':yearlist},
    markers=True,
    height=1200,
    width=600
)


mm = m.pivot(index=['氏名'],columns='年',values=obj_value).sort_values(year,ascending=False).reset_index()
mm.style.applymap("{:,.0}")

#
# Plot procedure
#

st.title(wardname+'区')
st.subheader('選挙概要')

show_summary = sum_tmp[['年','区名','定数','候補者数','有権者数','投票率%','投票者数']]

AgGrid.AgGrid(show_summary, fit_columns_on_grid_load=True,height=120)


st.subheader(obj_value + 'グラフ')
st.write("凡例は最新の選挙結果を降順に並べています。データは当選者のみです。凡例の候補者名をダブルクリックすると、グラフ全体が消え、その候補者だけを表示できます。その状態で、他の候補者をシングルクリックすると、その候補者のグラフが出現します。")

st.plotly_chart(fig, use_container_width=True)


st.subheader(obj_value + '表')
st.write("最新の選挙結果を降順に並べています。データは当選者のみです。ヘッダの年をクリックすると、その年のデータで並び替えられます。空欄は実績がないことを意味します。")
AgGrid.AgGrid(mm,fit_columns_on_grid_load=True,height=600)
