import os
import pandas as pd

def trace_topic(topic): # 话题名完全匹配
    time = []
    rank = []
    for csv_name in os.listdir('话题跟踪/'):
        df = pd.read_csv('话题跟踪/' + csv_name)
        if topic in list(df['话题']):
            time.append(str(df[df['话题']==topic]['时刻'].values[0]))
            rank.append(str(df[df['话题'] == topic]['排名'].values[0]))
            # res.append([str(df[df['话题']==topic]['时刻'].values[0]), str(df[df['话题']==topic]['排名'].values[0])]) # (时刻, 排名)
    return time, rank

def search_topic(topic): # 话题名部分匹配（包含关系）
    # res = []
    topic = []
    time = []
    rank = []
    for csv_name in os.listdir('话题跟踪/'):
        df = pd.read_csv('话题跟踪/' + csv_name)
        for i in list(df['话题']):
            if topic in i:
                topic.append(i)
                time.append(str(df[df['话题'] == topic]['时刻'].values[0]))
                rank.append(str(df[df['话题'] == topic]['排名'].values[0]))
                # res.append((i, str(df[df['话题']==i]['时刻'].values[0]), int(df[df['话题']==i]['排名'].values[0]))) # (话题, 时刻, 排名)
    return topic, time, rank

# 给定时域/话题的分地区舆情分析
def analyze_region(start_time='0', end_time='9', topic=None, search=False): # 时刻格式: '2023-05-25 11-04'
    region_list = ['河北', '山西', '吉林', '辽宁', '黑龙江', '陕西', '甘肃', '青海', '山东', 
                   '福建', '浙江', '河南', '湖北', '湖南', '江西', '江苏', '安徽', '广东', 
                   '海南', '四川', '贵州', '云南', '台湾', '北京', '上海', '天津', '重庆', 
                   '内蒙古', '新疆', '宁夏', '广西', '西藏', '香港', '澳门', '海外']
    region_dict = {}
    for region in region_list:
        region_dict[region] = [] # 这个列表存放所有的情感分
    for t in os.listdir('评论/'):
        if t >= start_time and t <= end_time:
            time_path = '评论/' + t
            if topic == None:
                for csv in os.listdir(time_path):
                    final_path = time_path + '/' + csv
                    df = pd.read_csv(final_path)
                    for i, v in enumerate(df['ip属地_省份']):
                        if v in region_list:
                            region_dict[v].append(int(df['情感'][i][-1]))
                        else:
                            region_dict['海外'].append(int(df['情感'][i][-1]))
            elif search == False:
                for csv in os.listdir(time_path):
                    if csv[:-4] == topic:
                        final_path = time_path + '/' + csv
                        df = pd.read_csv(final_path)
                        for i, v in enumerate(df['ip属地_省份']):
                            if v in region_list:
                                region_dict[v].append(int(df['情感'][i][-1]))
                            else:
                                region_dict['海外'].append(int(df['情感'][i][-1]))
            elif search == True:
                for csv in os.listdir(time_path):
                    if topic in csv[:-4]:
                        final_path = time_path + '/' + csv
                        df = pd.read_csv(final_path)
                        for i, v in enumerate(df['ip属地_省份']):
                            if v in region_list:
                                region_dict[v].append(int(df['情感'][i][-1]))
                            else:
                                region_dict['海外'].append(int(df['情感'][i][-1]))

    for region in region_dict:
        if len(region_dict[region]) == 0:
            continue
        else:
            region_dict[region] = sum(region_dict[region]) / len(region_dict[region])

    return region_dict

res = analyze_region(topic=None, search=True)

print(res)