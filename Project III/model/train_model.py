import os
import re
import pandas as pd
from nltk import ngrams
from sklearn import svm
from sklearn.externals import joblib
from underthesea import word_tokenize
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

emb = 0

# Load dữ liệu
def load_data():
    dt = pd.read_csv('data/dataset.csv', header = 0)
    
    return dt

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

# Embedding
def embedding(X_train, X_test):
    """
        min_df : loại bỏ những từ nào từ vocabulary có tần suất suất hiện nhỏ hơn min_df ( tính theo count)
        max_df " loại bỏ những từ nào từ vocabulary có tần suất xuất hiện lớn hơn max_df ( tính theo %)
        sublinear_tf: Scale term frequency bằng logarithmic scale
        max_features lựa chọn số character vào vocabulary
    """
    global emb
    emb = TfidfVectorizer(min_df = 5, max_df = 0.8, max_features = 3000, sublinear_tf = True)
    emb.fit(X_train)

    X_train = emb.transform(X_train)
    X_test = emb.transform(X_test)

    # Lưu vào file pkl
    joblib.dump(emb, 'model/tfidf.pkl')

    return X_train, X_test

# 1. Load dữ liệu
data = load_data()

# 2. Tiền xử lý dữ liệu và Tokenizer
data['Text'] = data.Text.apply(standardize_data)
data['Text'] = data.Text.apply(tokenizer)

# 3. Convert to X_train, y_train
"""
    random_state simply sets a seed to the random generator,
    so that your train-test splits are always deterministic.
    If you don't set a seed, it is different each time
"""
X_train, X_test, y_train, y_test = train_test_split(data['Text'], data['Sentiment'], test_size = 0.2, random_state = 42)

# 4. Embedding X_train
X_train, X_test = embedding(X_train, X_test)

# 5. Train và lưu model vào file pkl
model = svm.SVC(kernel = 'linear', C = 1)
model.fit(X_train, y_train)

joblib.dump(model, 'model/saved_model.pkl')

# 6. Test
print('Model Score = ', model.score(X_test, y_test))
print('Done')