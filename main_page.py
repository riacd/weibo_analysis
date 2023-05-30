import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import API
from threading import Thread
import pandas as pd
import analyze
from bokeh.plotting import figure
import numpy as np
import os

def sentiment_analysis_by_topic(time: str, topic: str):
    print('sentiment_analysis_by_topic: time(', time, ') topic(', topic, ')')
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
    print('sizes: ', sizes)
    st.pyplot(fig, clear_figure=True)
    print('sentiment plot_complete')

def auto_thread():
    f = os.popen('./main.py')

auto_button = st.sidebar.button('启动自动爬取')
if auto_button:
    st.sidebar.write('爬虫脚本运行中')
    t = Thread(target=lambda: os.popen('main.py'))
    t.start()

sentiment_analyze_tab, topic_hot_analyze_tab, topic_key_analyze_tab, topic_region_analyze_tab, topic_classification_analyze_tab = st.tabs(['评论情感分析', '话题热度分析','话题关键词分析', '话题区域及时域分析', '话题分类'])
time_list = API.weibo_analyse.get_time_list()
print(time_list)
with sentiment_analyze_tab:
    show_time = st.select_slider(
        "回溯时间",
        options=time_list,
        value=time_list[0],
        key=10)
    show_time_str = API.weibo_analyse.datetime2str(show_time)
    st.write("当前展示时间为", show_time_str)
    # topic_words = st.text_input(label='话题', value='上海迪士尼6月23日起门票调价', key=1)
    np_arr = API.weibo_analyse.read_csv('话题跟踪/'+show_time_str+'.csv')
    topic_array = [np_arr[i][0] for i in range(np_arr.shape[0])]
    topic_words = st.selectbox(label='话题', options=topic_array)
    sentiment_analyze_button = st.button("开始分析", key=2)
    if sentiment_analyze_button:
        sentiment_analysis_by_topic(show_time_str, topic_words)

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
    topic_key_words = st.text_input(label='话题关键词', value='上海迪士尼6月23日起门票调价')
    key_hot_button_clicked = st.button("开始分析", key=30)
    if key_hot_button_clicked:
        topic, time, rank = analyze.search_topic(topic_key_words)
        time = [str(API.weibo_analyse.str2datetime(time_str)) for time_str in time]
        np_data = np.array([topic, time, rank]).T

        print(np_data)
        chart_data = pd.DataFrame(
            np_data,
            columns=['topic', 'time', 'rank'])

        st.vega_lite_chart(chart_data, {
            'mark': {'type': 'circle', 'tooltip': True},
            'encoding': {
                'x': {'field': 'time', 'type': 'temporal'},
                'y': {'field': 'rank', 'type': 'quantitative'},
                # 'size': {'field': 'topic', 'type': 'nominal'},
                'color': {'field': 'topic', 'type': 'nominal'},
            },
        })


        st.vega_lite_chart(chart_data, {
            # 'mark': {'type': 'circle', 'tooltip': True},
            'mark': 'line',
            'encoding': {
                'x': {'field': 'time', 'type': 'temporal'},
                'y': {'field': 'rank', 'type': 'quantitative'},
                # 'size': {'field': 'topic', 'type': 'nominal'},
                'color': {'field': 'topic', 'type': 'nominal'},
            },
        })


with topic_region_analyze_tab:
    start_time, end_time = st.select_slider(
    label="时间区段",
    options=time_list,
    value=(time_list[0], time_list[2]), key=101)
    topic_words = st.text_input(label='话题', value='上海迪士尼6月23日起门票调价', key=15)
    search_flag = st.checkbox(label='模糊搜索')
    region_button_clicked = st.button("开始分析", key=12)
    if region_button_clicked:
        region_dict = analyze.analyze_region(start_time, end_time, topic_words, search_flag)
        print(region_dict)
        st.dataframe(region_dict, width=700)

with topic_classification_analyze_tab:
    start_time_, end_time_ = st.select_slider(
    label="时间区段",
    options=time_list,
    value=(time_list[0], time_list[2]), key=102)
    classification_button_clicked = st.button("开始分析", key=13)
    if classification_button_clicked:
        classification_dict = analyze.topic_classification(start_time_, end_time_)
        sizes_ = classification_dict.values()
        labels = ['financial news', 'International news', 'mainland China politics', 'culture', 'entertainment', 'sports', 'others']
        plt.pie(sizes_, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)  # '%1.1f'：指小数点后保留一位有效数值；'%1.2f%%'保留两位小数点，增加百分号（%）;startangle=90则从y轴正方向画起
        plt.axis('equal')  # 该行代码使饼图长宽相等
        plt.title('trending topic classification', fontdict={'size': 15})
        plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)  # 添加图例
        st.pyplot(fig, clear_figure=True)









