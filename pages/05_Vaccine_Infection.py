import os
import pathlib
import pandas as pd
import plotly.express as px
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

text="""
* 情報源

ワクチン接種者（1〜6回目接種者全て）

デジタル庁 ワクチン接種記録システム（VRS）

https://info.vrs.digital.go.jp/dashboard/

COVID19新規陽性者

厚生労働省 新型コロナウィルス感染症について・オープンデータ

https://www.mhlw.go.jp/stf/covid-19/open-data.html

* ワクチン接種開始時期

第１・２回 2021年 2月17日

第３回 2021年12月 1日

第４回 2022年 5月27日

第５回 2022年10月

第６回 2023年 5月11日

接種者の分布と新規陽性者の分布（山のある時期）がほぼ同期していることに注意。ワクチン接種後、しばらくすると免疫力がさがることがあるようだ。
"""
st.markdown(text)
st.plotly_chart(distp(pref), use_container_width=True)




