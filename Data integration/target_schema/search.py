from collections import Counter
import math
import re
import editdistance
import gensim
import mysql.connector
import unidecode

#Connect mysql
mydb = mysql.connector.connect(
    host="freedb.tech",
    user="freedbtech_doan",
    password="doan",
    database="freedbtech_DoAn"
)
mycursor = mydb.cursor()

#Xóa dấu tiếng việt
def remove_accent(text):
    return unidecode.unidecode(text)

#Xóa ký tự thừa
def removeKyTuThua(text):
    senteces = ""
    arr = gensim.utils.simple_preprocess(text)
    for i in arr:
        senteces=senteces+i+" "
    return senteces

#So sánh editdistance giữa 2 văn bản
def editDistance2sentences(text1,text2):
    text1 = removeKyTuThua(text1)
    text2 = removeKyTuThua(text2)
    text1 = remove_accent(text1)
    text2 = remove_accent(text2)
    return editdistance.eval(text1,text2)

#Lấy văn bản gần nhất
def nearestEditDistance(text,copus):
    min = 1000000
    sentences = ""
    for i in range(len(copus)):
        distance = editDistance2sentences(text,copus[i])
        if distance<min:
            min=distance
            sentences = copus[i]
    return min,sentences

#Công thức cosin
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

#Chuyển text sang vector
def text_to_vector(text):
    word = re.compile(r'\w+')
    text = remove_accent(text)
    words = word.findall(text)
    return Counter(words)

#So sánh 2 câu
def cosinSimilar2sentences(content_a, content_b):
    vector1 = text_to_vector(content_a)
    vector2 = text_to_vector(content_b)
    cosine_result = get_cosine(vector1, vector2)
    return cosine_result

#Hàm search
def searchItem(name):
    #Category
    category = ['iphone', 'samsung', 'xiaomi', 'oppo', 'vsmart', 'realme', 'vivo','nokia', 'huawei']
    #Tìm category của name
    y = nearestEditDistance(name,category)
    y = str(y[1]).upper()
    #Duyệt trong mysql category tương ứng
    sql = "select name from product where category = %s"
    val = [y]
    mycursor.execute(sql,val)
    myresult = mycursor.fetchall()

    #Mảng arr sẽ chứa tất cả đthoai của category đó
    arr = []
    for i in myresult:
        arr.append(i[0])

    #result sẽ chứa tất cả điện thoại được tìm ra xếp theo độ tương đồng
    result = {}
    for i in arr:
        #Tính độ tương đồng
        similar = cosinSimilar2sentences(name,i)
        if similar >0.1:
            result[i] = similar

    result = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    return result

import time    

input= input()
t= time.time()
result = searchItem(input)
t1= time.time()
print(t1-t)
print(result)