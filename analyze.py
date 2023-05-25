import os
import pandas as pd

def trace_topic(topic): # 话题名完全匹配
    res = []
    for csv_name in os.listdir('话题跟踪/'):
        df = pd.read_csv('话题跟踪/' + csv_name)
        if topic in list(df['话题']):
            res.append((str(df[df['话题']==topic]['时刻'].values[0]), int(df[df['话题']==topic]['排名']))) # (时刻, 排名)
    return res

def search_topic(topic): # 话题名部分匹配（包含关系）
    res = []
    for csv_name in os.listdir('话题跟踪/'):
        df = pd.read_csv('话题跟踪/' + csv_name)
        for i in list(df['话题']):
            if topic in i:
                res.append((i, str(df[df['话题']==i]['时刻'].values[0]), int(df[df['话题']==i]['排名']))) # (话题, 时刻, 排名)
    return res

print(search_topic('女生'))