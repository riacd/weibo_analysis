import streamlit as st
from datetime import datetime

import API

show_time = st.sidebar.slider(
    "展示时间",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm")
show_time_str = API.weibo_analyse.datetime2str(show_time)
st.write("当前展示时间为", show_time_str)
key_words = st.text_input(label='关键词')
time_str = '2023-05-25 11-04'
st.button("开始分析", on_click=API.call_analyse_key, args=[time_str, key_words])
st.pyplot(API.fig)

