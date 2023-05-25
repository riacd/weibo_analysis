import API

if __name__ == '__main__':
    a = API.weibo_analyse()
    a.add_sentiment('./csv/微博清单_浙江59岁孕妇成功产下一女婴_前5页.csv')