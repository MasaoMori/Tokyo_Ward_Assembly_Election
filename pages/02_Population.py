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
wardlist = ['中央', '台東', '品川', '目黒', '大田', '渋谷']
wardname = st.sidebar.selectbox("対象区名", wardlist)

#
# Plot procedure

st.title(wardname+'区')
st.subheader('人口概要')
st.write('準備中')
