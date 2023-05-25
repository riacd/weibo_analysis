import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import API
from threading import Thread
import pandas as pd
import analyze
from bokeh.plotting import figure
import numpy as np

fig = plt.figure()


def sentiment_analysis_by_topic(time: str, topic: str):
    print('sentiment_analysis_by_topic')
    path = './评论/' + time + '/' + topic + '.csv'
    sizes = [0, 0, 0, 0, 0]
    pd_data = pd.read_csv(path)
    for index, row in pd_data.iterrows():
        for star in range(5):
            if row['情感'] == 'star ' + str(star + 1):
                sizes[star] += 1
    labels = ['very_negative', 'negative', 'neutral', 'positive', 'very_positive']
    plt.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)  # '%1.1f'：指小数点后保留一位有效数值；'%1.2f%%'保留两位小数点，增加百分号（%）;startangle=90则从y轴正方向画起
    plt.axis('equal')  # 该行代码使饼图长宽相等
    plt.title('comment sentiment', fontdict={'size': 15})
    plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)  # 添加图例
    print('OK')

def call_analyse_key(time: str, key: str):
    t = Thread(target=sentiment_analysis_by_topic, args=[time, key])
    t.start()



topic_analyze_tab, topic_hot_analyze_tab, topic_key_analyze_tab, topic_region_analyze_tab = st.tabs(['话题分析', '话题热度分析','话题关键词分析', '话题区域及时域分析'])
with topic_analyze_tab:
    show_time = st.select_slider(
        "展示时间",
        options=API.weibo_analyse.get_time_list(),
        key=10)
    show_time_str = API.weibo_analyse.datetime2str(show_time)
    st.write("当前展示时间为", show_time_str)
    topic_words = st.text_input(label='话题', key=1)
    time_str = '2023-05-25 18-18'
    st.button("开始分析", key=2, on_click=call_analyse_key, args=[time_str, topic_words])
    st.pyplot(fig, clear_figure=False)

with topic_hot_analyze_tab:
    topic_hot_words = st.text_input(label='话题', key=3, value='上海迪士尼6月23日起门票调价')
    button_clicked = st.button("开始分析")
    if button_clicked:
        times, ranks = analyze.trace_topic(topic_hot_words)
        times = [API.weibo_analyse.str2datetime(time) for time in times]
        p = figure(
            title='话题排名变动',
            x_axis_label='时间',
            y_axis_label='排名')
        p.line(times, ranks, legend_label='趋势', line_width=2)

        st.bokeh_chart(p)



with topic_key_analyze_tab:
    topic_key_words = st.text_input(label='话题关键词')
    st.button("开始分析", key=4, on_click=call_analyse_key, args=[time_str, topic_key_words])

    region_dict = analyze.analyze_region(topic=topic_key_words)

    chart_data = pd.DataFrame(
        np.random.randn(200, 3),
        columns=['time', 'rank', 'topic'])

    st.vega_lite_chart(chart_data, {
        'mark': {'type': 'circle', 'tooltip': True},
        'encoding': {
            'x': {'field': 'time', 'type': 'quantitative'},
            'y': {'field': 'rank', 'type': 'quantitative'},
            'size': {'field': 'topic', 'type': 'quantitative'},
            'color': {'field': 'topic', 'type': 'quantitative'},
        },
    })


with topic_region_analyze_tab:
    start_time, end_time = st.select_slider(
    label="时间区段",
    options=API.weibo_analyse.get_time_list(),
    value=('2023-05-25 11-04', '2023-05-25 18-18'))
    topic_words = st.text_input(label='话题', key=5)
    search_flag = st.checkbox(label='模糊搜索')
    region_button_clicked = st.button("开始分析", key=12)
    if region_button_clicked:
        analyze.analyze_region(start_time, end_time, topic_words, search_flag)






