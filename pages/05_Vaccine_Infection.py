import os
import pathlib
import pandas as pd
import plotly.express as px
import ndjson
import locale
import streamlit as st

cpath = os.getcwd()
ppath = str(pathlib.Path(cpath))

#####
vc = pd.read_csv(ppath + '/data/vc.csv')
pref = pd.read_csv(ppath + '/data/pref.csv')

gtitle =  '接種者と新規陽性者 2021/4 ~ 2023/4'
st.subheader(gtitle)
pref = st.sidebar.selectbox('都道府県名',list(pref['都道府県名']))

def distp(p):
    condition = (vc['都道府県名']==pref)&(vc['日付']>='2021/4/1')&(vc['日付']<='2023/4/30')

    all_country=vc[condition]
    fig=px.line(all_country, x='日付', y='人数', color='カテゴリ',#barmode='group',
                width=1400,height=800, title=pref+gtitle)
    fig.update_xaxes(dtick="M1",tickformat="%m\n%Y")
    fig.update_yaxes(tickformat=',')
    fig.add_annotation(x='2021-12-1', y=0,text="第3回接種開始",showarrow=True, ay=30)
    fig.add_annotation(x='2022-5-27', y=0,text="第4回接種開始",showarrow=True, ay=30)
    fig.add_annotation(x='2022-9-30', y=0,text="第5回接種開始",showarrow=True, ay=30)

    return fig

st.plotly_chart(distp(pref), use_container_width=True)




