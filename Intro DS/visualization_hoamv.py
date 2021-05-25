# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:31:23 2020

@author: Mai Van Hoa
"""

import numpy as np
import pandas as pd
from pandas import read_csv
import math
import matplotlib.pyplot as plt

filename = 'dataset.csv'
data = read_csv(filename)
# types = data.dtypes
# print(types)

# doanh thu qua các năm
def release_gross():
    d = data[['release', 'gross']].values

    for i in range(len(d)):
        if type(d[i][1]) is not str:
            d[i][1] = 0
        else:
            d[i][1] = int(d[i][1].replace(',','').replace('.',''))
    
    rg = dict()
    for i in range(len(d)):
        if d[i][0] not in rg:
            rg[d[i][0]] = 0
        else:
            rg[d[i][0]] += d[i][1]
    
    rg = sorted(rg.items(), key=lambda x: x[0])
    x = []
    y = []
    
    for i in range(len(rg)):
        x.append(rg[i][0])
        y.append(rg[i][1])
    #print(x, y)    
    plt.plot(x, y)
    plt.xlabel('Release')
    plt.ylabel('Gross')


# doanh thu theo thể loại
def genre_gross():
    d = data[['genre', 'gross']].values
    
    for i in range(len(d)):
        if type(d[i][1]) is not str:
            d[i][1] = 0
        else:
            d[i][1] = int(d[i][1].replace(',','').replace('.',''))
            
    gg = dict()
    for i in range(len(d)):
        s = d[i][0].split(', ')
        for j in range(len(s)):
            if s[j] not in gg:
                gg[s[j]] = 0
            else:
                gg[s[j]] += d[i][1]
    
    genre = gg.keys()
    gross = gg.values()
    y_pos = np.arange(len(genre))
    
    plt.figure(figsize=(16,9))
    # create horizontal bars
    plt.barh(y_pos, gross)
    
    # create names on the y-axis
    plt.yticks(y_pos, genre)
    plt.xlabel('Gross')
    plt.ylabel('Genre')

if __name__ == '__main__':
    release_gross()
    genre_gross()
    





























