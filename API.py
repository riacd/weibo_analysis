from threading import Thread
from transformers import AutoModelForSequenceClassification,AutoTokenizer,pipeline
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import re
import os





class model_tagger:
    def __init__(self):
        self.topic_classification_model = AutoModelForSequenceClassification.from_pretrained('uer/roberta-base-finetuned-chinanews-chinese')
        self.topic_classification_tokenizer = AutoTokenizer.from_pretrained('uer/roberta-base-finetuned-chinanews-chinese')
        self.topic_classification_text_classification = pipeline('sentiment-analysis', model=self.topic_classification_model, tokenizer=self.topic_classification_tokenizer)
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained('techthiyanes/chinese_sentiment')
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained('techthiyanes/chinese_sentiment')
        self.sentiment_text_classification = pipeline('sentiment-analysis', model=self.sentiment_model, tokenizer=self.sentiment_tokenizer)

    def sentiment_tag(self, string):
        output = self.sentiment_text_classification(string)
        out=[dic['label'] for dic in output]
        return out

    def topic_tag(self, key):
        output = self.topic_classification_text_classification(key)
        out=[dic['label'] for dic in output]
        return out

    def add_sentiment(self, path: str):
        Data = pd.read_csv(path)
        List = []
        for index, row in Data.iterrows():
            List.append(self.sentiment_tag(row['微博内容'])[0])
        Data['情感'] = List  # 注明列名，就可以直接添加新列
        Data.to_csv(path, index=False)  # 把数据写入数据集，index=False表示不加索引
        # 注意这里的ngData['length']=ngList是直接在原有数据基础上加了一列新的数据，也就是说现在的ngData已经具备完整的3列数据
        # 不用再在to_csv中加mode=‘a’这个参数，实现不覆盖添加。



class weibo_analyse:
    def __init__(self):
        self.database = {}

    @staticmethod
    def read_csv(path):
        return np.array(pd.read_csv(path))

    @staticmethod
    def get_time_list():
       return [t for t in os.listdir('评论/')]


    @staticmethod
    def datetime2str(datetime_obj):
        return str(datetime_obj)[:16].replace(':', '-')

    @staticmethod
    def str2datetime(datetime_str):
        args = re.split('[^0123456789]+', datetime_str)
        args = [int(arg) for arg in args]
        return datetime.datetime(*args)

    @staticmethod
    def sentiment_analysis_by_topic(time: str, topic: str):
        print('sentiment_analysis_by_topic')
        path = './评论/'+time+'/'+topic+'.csv'
        sizes = [0, 0, 0, 0, 0]
        pd_data = pd.read_csv(path)
        for index, row in pd_data.iterrows():
            for star in range(5):
                if row['情感'] == 'star '+str(star+1):
                    sizes[star]+=1
        labels = ['消极', '较消极', '中性', '较积极', '积极']
        global fig
        plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)  # '%1.1f'：指小数点后保留一位有效数值；'%1.2f%%'保留两位小数点，增加百分号（%）;startangle=90则从y轴正方向画起
        plt.axis('equal')  # 该行代码使饼图长宽相等
        plt.title('话题评论情感占比', fontdict={'size': 15})
        plt.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)  # 添加图例
        # plt.show()
        print('OK')


    def sentiment_analysis_by_topic_region(self, topic):
        pass

    def sentiment_analysis_by_region(self):
        pass

    def topic_classification_with_time(self):
        pass

if __name__ == '__main__':
    print(weibo_analyse.str2datetime('2023-05-25 21-12'))