import requests
from bs4 import BeautifulSoup
import re
import time
import os
from jsonpath import jsonpath  # 解析json数据
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用
import numpy as np
import API
import torch

def get_topics():
    url = r'https://www.weibo.cn/'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"}
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.text, 'lxml')
    raw_topics = re.findall(r'>\#.+?\#</a>', str(soup))
    topics = []
    for i, v in enumerate(raw_topics):
        topics.append(v[2:-5])
    return topics

def get_comments(keyword, max_page, time, model_tagger):
    """
    爬取微博内容列表
    :param keyword: 搜索关键字
    :param max_page: 爬取几页
    :return: None
    """
    def trans_time(v_str):
        """转换GMT时间为标准格式"""
        GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
        timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
        ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
        return ret_time

    def getLongText(v_id, headers):
        """爬取长微博全文"""
        url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
        r = requests.get(url, headers=headers)
        json_data = r.json()
        long_text = json_data['data']['longTextContent']
        # 微博内容-正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        long_text2 = dr.sub('', long_text)
        # print(long_text2)
        return long_text2

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }

    file_name = '{}.csv'.format(keyword)

    path = '评论/' + time + '/' + file_name

    if not os.path.exists('评论'):
        os.mkdir('评论')

    if not os.path.exists('评论/' + time):
        os.mkdir('评论/' + time)

    # # 如果csv文件存在，先删除之
    # if os.path.exists(file_name):
    #     os.remove(file_name)
    #     print('微博清单存在，已删除: {}'.format(file_name))

    for page in range(2, max_page + 2):
        print('===开始爬取第{}页微博==='.format(page))
        # 请求地址
        url = 'https://m.weibo.cn/api/container/getIndex'
        # 请求参数
        params = {
            "containerid": "100103type=1&q={}".format(keyword),
            "page_type": "searchall",
            "page": page
        }
        # 发送请求
        r = requests.get(url, headers=headers, params=params)
        print(r.status_code)
        # pprint(r.json())
        # 解析json数据
        cards = r.json()["data"]["cards"]
        print(len(cards))
        region_name_list = []
        status_city_list = []
        status_province_list = []
        status_country_list = []
        for card in cards:
            # 发布于
            try:
                region_name = card['card_group'][0]['mblog']['region_name']
                region_name_list.append(region_name)
            except:
                region_name_list.append('')
            # ip属地_城市
            try:
                status_city = card['card_group'][0]['mblog']['status_city']
                status_city_list.append(status_city)
            except:
                status_city_list.append('')
            # ip属地_省份
            try:
                status_province = card['card_group'][0]['mblog']['status_province']
                status_province_list.append(status_province)
            except:
                status_province_list.append('')
            # ip属地_国家
            try:
                status_country = card['card_group'][0]['mblog']['status_country']
                status_country_list.append(status_country)
            except:
                status_country_list.append('')
        # 微博内容
        text_list = jsonpath(cards, '$..mblog.text')
        # 微博内容-正则表达式数据清洗
        dr = re.compile(r'<[^>]+>', re.S)
        text2_list = []
        print('text_list is:')
        # print(text_list)
        if not text_list:  # 如果未获取到微博内容，进入下一轮循环
            continue
        if type(text_list) == list and len(text_list) > 0:
            for text in text_list:
                text2 = dr.sub('', text)  # 正则表达式提取微博内容
                # print(text2)
                text2_list.append(text2)
        # 情感
        sentiment_list = model_tagger.sentiment_tag(text2_list)
        # 微博创建时间
        time_list = jsonpath(cards, '$..mblog.created_at')
        time_list = [trans_time(v_str=i) for i in time_list]
        # 微博作者
        author_list = jsonpath(cards, '$..mblog.user.screen_name')
        # 微博id
        id_list = jsonpath(cards, '$..mblog.id')
        # 判断是否存在全文
        isLongText_list = jsonpath(cards, '$..mblog.isLongText')
        idx = 0
        for i in isLongText_list:
            if i == True:
                long_text = getLongText(id_list[idx], headers)
                text2_list[idx] = long_text
            idx += 1
        # 转发数
        reposts_count_list = jsonpath(cards, '$..mblog.reposts_count')
        # 评论数
        comments_count_list = jsonpath(cards, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count')
        # 把列表数据保存成DataFrame数据
        print('id_list:', len(id_list))
        print(len(time_list))
        print('region_name_list:', len(region_name_list))
        print(len(status_city_list))
        print(len(status_province_list))
        print(len(status_country_list))

        df = pd.DataFrame(
            {
                '页码': [page] * len(id_list),
                '微博id': id_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '微博内容': text2_list,
                '转发数': reposts_count_list,
                '评论数': comments_count_list,
                '点赞数': attitudes_count_list,
                '发布于': region_name_list,
                'ip属地_城市': status_city_list,
                'ip属地_省份': status_province_list,
                'ip属地_国家': status_country_list,
                '情感': sentiment_list
            }
        )
        # 表头
        if os.path.exists(path):
            header = None
        else:
            header = ['页码', '微博id', '微博作者', '发布时间', '微博内容', '转发数', '评论数',
                      '点赞数', '发布于', 'ip属地_城市', 'ip属地_省份', 'ip属地_国家', '情感']  # csv文件头
        # 保存到csv文件

        df.to_csv(path, mode='a+', index=False,
                  header=header, encoding='utf_8_sig')
        print('csv保存成功:{}'.format(file_name))

    # 数据清洗-去重
    df = pd.read_csv(path)
    # 删除重复数据
    df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
    # 再次保存csv文件
    df.to_csv(path, index=False, encoding='utf_8_sig')
    print('数据清洗完成')

def mainloop(model_tagger):
    while True:
        t = str(datetime.datetime.now())[:-10].replace(':', '-')
        # 话题简单跟踪
        file_name = '话题跟踪/' + t + '.csv'
        topics = get_topics()
        topic_list = topics
        rank_list = list(np.arange(len(topic_list)))
        time_list = [t] * len(topic_list)
        topic_tag_list = model_tagger.topic_tag(topic_list)
        df = pd.DataFrame(
            {
                '话题': topic_list,
                '排名': rank_list,
                '时刻': time_list,
                '话题分类': topic_tag_list
            }
        )
        if os.path.exists(file_name):
            header = None
        else:
            header = ['话题', '排名', '时刻', '话题分类']  # csv文件头
        df.to_csv(file_name, mode='a+', index=False, header=header, encoding='utf_8_sig')
        
        # 话题评论留档
        for topic in topics:
            get_comments(topic, 5, t, model_tagger)
            time.sleep(1) # 稍微有点怕被反爬
        
        # 休息一会（微博热榜每十分钟刷新一次）
        time.sleep(600)

if __name__ == '__main__':
    model_tagger = API.model_tagger()
    mainloop(model_tagger)