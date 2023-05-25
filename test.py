import API
# import datetime

if __name__ == '__main__':
    model_tagger = API.model_tagger()
    model_tagger.add_sentiment('./评论/2023-05-25 11-04/24岁研究生离世捐器官救多人.csv')