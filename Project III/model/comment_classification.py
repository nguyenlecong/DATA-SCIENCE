import os
import re
import csv
import json
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from underthesea import word_tokenize

# Load URL
def load_data():

    data = pd.read_csv('data/test.csv', header = 0)

    return data

# Tiền xử lý dữ liệu
def standardize_data(row):
    # Xóa các ký tự đặc biệt:
    row = re.sub(r'[\.,\?]+$-', '', row)
    special_characters = ('~','`','!','@','#','$','%','^','&','*','(',')','_','-','=','+','{','}','[',']',':',';','"',',','<','.','>','?','/','|')
    
    for i in special_characters:
        row = row.replace(i, " ")

    row = row.strip()

    return row

# Tokenizer
def tokenizer(row):
    return word_tokenize(row, format = 'text')

# Thống kê
def analyze(result, data):
    positive = np.count_nonzero(result)
    negative = len(result) - positive

    print('Số bình luận đồng ý: ', positive)
    print('Số bình luận không đồng ý: ', negative)

    res = [idx for idx, val in enumerate(result) if val == 0] 
    for i in range(len(res)):
        if res[i] == i:
            sentiment = 'Không đồng ý'
            print(data[i], ': ', sentiment)
        else:
            sentiment = 'Đồng ý'
            print(data[i], ': ', sentiment)

# Lưu kết quả ra file
    #     with open('data/result.csv', mode='a', encoding='utf-8', newline='') as file:
    #         writer = csv.writer(file, delimiter=',')
    #         writer.writerow([data[i], sentiment])
    # file.close()

    # df = pd.read_csv('data/result.csv', header=None)
    # df.columns = ['Text', 'Sentiment']
    # df.to_csv('data/result.csv')

# 1. Load data
data = load_data()

# 2. Tiền xử lý dữ liệu và Tokenizer
data['Text'] = data.Text.apply(standardize_data)
data['Text'] = data.Text.apply(tokenizer)

# 4. Embedding
X_val = data['Text']
emb = joblib.load('model/tfidf.pkl')
X_val = emb.transform(X_val)

# 5. Phân loại
model = joblib.load('model/saved_model.pkl')
result = model.predict(X_val)

# 6. Thống kê
analyze(result, data['Text'])
