from threading import Thread
from transformers import AutoModelForSequenceClassification,AutoTokenizer,pipeline
import pandas as pd
import numpy as np
from datetime import datetime


def call_analyse_key(key: str):
    t = Thread(target=analyse_key, args=[key])
    t.start()

def analyse_key(key: str):
    pass

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


class weibo_analyse:
    def __init__(self):
        self.database = {}


    def read_csv(self, path):
        return np.array(pd.read_csv(path))

    def datetime2str(self, time):
        date_str = str(time.date.year)+'-'+str(time.date.month)+'-'+str(time.date.day)+' '+str(time.hour)+'-'+str(time.minute)
        return date_str

    def add_sentiment(self, path: str):
        Data = pd.read_csv(path)
        List = []
        for index, row in Data.iterrows():
            List.append(self.sentiment_tag(row['微博内容'])[0])
        Data['情感'] = List  # 注明列名，就可以直接添加新列
        Data.to_csv('path', index=False)  # 把数据写入数据集，index=False表示不加索引
        # 注意这里的ngData['length']=ngList是直接在原有数据基础上加了一列新的数据，也就是说现在的ngData已经具备完整的3列数据
        # 不用再在to_csv中加mode=‘a’这个参数，实现不覆盖添加。

    def sentiment_analysis_by_topic(self, topic, time):
        pass

    def sentiment_analysis_by_topic_region(self, topic):
        pass

    def sentiment_analysis_by_region(self):
        pass

    def topic_classification_with_time(self):
        pass