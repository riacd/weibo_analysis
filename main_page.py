import streamlit as st

import API

key_words = st.text_input(label='关键词')
st.button("开始分析", on_click=API.call_analyse_key, args=[key_words])
