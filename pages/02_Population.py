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

#### サイドバーでパラメータを決める
#wardlist = ['中央', '台東', '品川', '目黒', '大田', '渋谷']
#wardname = st.sidebar.selectbox("対象区名", wardlist)

#
# Plot procedure


result = pd.read_csv(cpath + '/data/2021年区別年齢別人口分布.csv')
d15 = pd.read_csv(cpath + '/data/2009-2021区別15歳人口推移.csv')

tokyocode = pd.read_csv(cpath + '/data/tokyo_code.csv').rename(columns={'団体コード':'地域コード','団体名':'地域'})
sorted_wards = list(tokyocode[(131000 <tokyocode['地域コード']) & (tokyocode['地域コード']<132000)]['地域'])

def lim_ward(d):
    return d[(131000 <d['地域コード']) & (d['地域コード']<132000)]


##
## 老年者（65歳以上）人口
##
older_people =lim_ward(result[result['age']>64])
otext_data = list(older_people.groupby(['地域コード','地域']
                           ).sum('人口').reset_index().drop(columns='age').sort_values('地域コード')['人口'])

fig_old = px.bar(
    older_people,
    y='地域',
    x='人口',
    title='65歳以上人口',
    category_orders={'地域':sorted_wards},
    height=800,
    width=900,
    orientation='h',
    range_x=(0,200000)
)
fig_old.data[0].text = list(map((lambda x: '{:,d}'.format(x)), otext_data))
fig_old.data[0]['hovertemplate'] ='人口=%{x:,d}'+'<br>地域=%{y}'



##
## 18から27歳人口
##
younger_people = lim_ward(result[(result['age']>17)&(65>result['age'])])
text_data = list(younger_people.groupby(['地域コード','地域']
                                  ).sum('人口').reset_index().drop(columns='age').sort_values('地域コード')['人口'])

fig_young = px.bar(
    younger_people,
    x='人口',
    y='地域',
    title='18〜27歳人口（推計・トップの数は総和）',
    color='年齢',
    height=800,
    width=920,
    category_orders={'地域':sorted_wards},
    color_discrete_sequence = px.colors.sequential.dense_r,
    orientation='h',
    range_x=(0,200000),
)

fig_young.data[-1].text = list(map((lambda x: '{:,}'.format(x)), text_data))


##
## 15歳人口推移
##

fig_fifteen = px.line(
    lim_ward(d15).sort_values('年'),
    x='年',
    y='15歳人口',
    text='15歳人口',
    title='15歳人口の推移',
    color='地域',
    category_orders={'地域':sorted_wards,
                     'y_n+1':list(range(2009,2021,1))},
    markers=True,
    height=800,
    width=1000
)



fig_old.update_traces(textposition='outside')
fig_young.update_traces(textposition='outside')

# AgGrid.AgGrid(summary[summary['区名']==wardname],fit_columns_on_grid_load=True,height=120)
st.subheader('老年者（65歳以上）人口分布（2021年）')
st.write("")
st.plotly_chart(fig_old, use_container_width=True)
st.subheader('18〜27歳人口分布（2021年）')
st.write("")
st.plotly_chart(fig_young, use_container_width=True)
#AgGrid.AgGrid(mm,fit_columns_on_grid_load=True,height=600)

st.subheader('参考：15歳人口経年推移')
st.write("")
st.plotly_chart(fig_fifteen, use_container_width=True)

