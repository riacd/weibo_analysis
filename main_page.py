import streamlit as st
from datetime import datetime

import API

show_time = st.slider(
    "When do you start?",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm")
st.write("当前展示时间为", show_time)
key_words = st.text_input(label='关键词')
st.button("开始分析", on_click=API.call_analyse_key, args=[key_words])
