from __future__ import print_function
import numpy as np 
import pandas as pd 
from pandas import DataFrame
import math
import matplotlib.pyplot as plt
# n_cols = ['title','release','certificate','runtime','genre','rating','director','star','votes','Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Sport','Talk-Show','Thriller','War','Western']

movie = pd.read_csv('imdbdata/dataset.csv', sep = ',',encoding='latin-1')
m_col = movie.values

# print(m_col)

def findMode(a):
	_, idx, counts = np.unique(a, return_index=True, return_counts=True)
	index = idx[np.argmax(counts)]
	mode = a[index]
	return mode

def split(a, axis):
	list_ = list()
	for i in range(a.shape[0]):
		if a[i][axis] not in list_ : list_.append(a[i][axis])
	return list_

def visualize_Alone(a, axis, title):
	m = np.array(split(a, axis))
	print(m.shape[0])
	print(m)
	count = np.zeros((m.shape[0],))
	for i in range(m.shape[0]):
		for j in range(a.shape[0]):
			if m[i] == a[j][axis]: count[i] += 1
	print("max: ",np.max(count))
	print("min: ",np.min(count))
	print("mean: ",np.mean(count))
	print("mode: ",findMode(count))
	fig, axs = plt.subplots(figsize=(9, 3), sharey=True)
	axs.bar(m, count)
	axs.set_title(title)
	plt.show()

def visualize_with_vote_or_rating(a, axis, col, title):
	dict_ = dict()
	for i in range(a.shape[0]):
		if a[i][axis] not in dict_: 
			dict_[a[i][axis]] = list()
			dict_[a[i][axis]].append(a[i][col])
		else: dict_[a[i][axis]].append(a[i][col])
	name = np.array(list(dict_.keys()))
	print(name.shape)
	max_ = np.zeros((name.shape[0],))
	min_ = np.zeros((name.shape[0],))
	mean_ = np.zeros((name.shape[0],))
	mode_ = np.zeros((name.shape[0],))
	for i in range(name.shape[0]):
		if name[i] == 'nan': continue
		m = np.array(dict_[name[i]])
		max_[i] = m.max()
		min_[i] = m.min()
		mean_[i] = m.mean()
		mode_[i] = findMode(m)
	if col == 8: title_ = ' vote in '+title 
	else: title_ = ' rating in '+title
	fig, axs0 = plt.subplots(figsize=(9, 3), sharey=True)
	axs0.bar(name, max_)
	axs0.set_title('The max amount of '+title_)
	fig, axs1 = plt.subplots(figsize=(9, 3), sharey=True)
	axs1.bar(name,min_)
	axs1.set_title('The min amount of '+title_)
	fig, axs2 = plt.subplots(figsize=(9, 3), sharey=True)
	axs2.bar(name, mean_)
	axs2.set_title('The mean amount of '+title_)
	fig, axs3 = plt.subplots(figsize=(9, 3), sharey=True)
	axs3.bar(name, mode_)
	axs3.set_title('The mode amount of '+title_)
	plt.show()


#visualize the years
visualize_Alone(m_col,1,'The number of movies in years')
#visualize the cerfiticate
visualize_Alone(m_col,2,'The number of movies in cerfiticates')
# visualize the time
visualize_Alone(m_col,3,'The number of movies in runtime')
# visualize the vote in years
visualize_with_vote_or_rating(m_col, 1, 10,'years')
# #visualize the vote in cerfiticate
visualize_with_vote_or_rating(m_col, 2, 10,'cerfiticates')
# visualize the rating in years
visualize_with_vote_or_rating(m_col, 1, 5,'years')
# visualize the rating in cerfiticate
visualize_with_vote_or_rating(m_col, 2, 5,'cerfiticates')

#visualize the movies
print('number of movie', movie.shape)
m = list()
v = list()
r = list()
for i in range(m_col.shape[0]):
	m.append(m_col[i][0])
	r.append(m_col[i][5])
	v.append(m_col[i][10])
m = np.array(m)
r = np.array(r)
v = np.array(v)
print('max rating: ',r.max())
print('min rating: ',r.min())
print('mean rating: ',r.mean())
print('mode rating: ',findMode(r))
print('max voting: ',v.max())
print('min voting: ',v.min())
print('mean voting: ',v.mean())
print('mode voting: ',findMode(v))

def sum_genr(genre, col):
	return np.sum(genre[:,col])
genr = np.array(['Action','Adventure','Animation','Biography','Comedy','Crime','Documentary','Drama','Family','Fantasy','Film-Noir','Game-Show','History','Horror','Music','Musical','Mystery','News','Reality-TV','Romance','Sci-Fi','Sport','Talk-Show','Thriller','War','Western'])
list_ = list()
print(genr.shape[0])
# count the number of movie by genr
for i in range(26):
	list_.append(sum_genr(m_col,i+12))
# visualize rating and voting for genr
def visualize_with_vote_or_rating_genr(a, axis, col):
	list_ = list()
	for i in range(a.shape[0]):
		if a[i][axis] == 1: list_.append(a[i][col])
	name = np.array(list_)
	return name
m = np.array(list_)
for i in range(genr.shape[0]):
	print(str(genr[i])+' : '+str(m[i]))
fig, axs0 = plt.subplots(figsize=(9, 3), sharey=True)
# print(list_)
axs0.bar(genr, np.array(list_))
plt.show()
# visualize the vote for genr
m = list([6,11,17,18,22])
mix_ = np.zeros((26,4))
for i in range(26):
	if i in m:
		mix_[i][:] = 0 
		continue	
	mix_[i][0] += visualize_with_vote_or_rating_genr(m_col,12+i,10).max()
	mix_[i][1] += visualize_with_vote_or_rating_genr(m_col,12+i,10).min()
	mix_[i][2] += visualize_with_vote_or_rating_genr(m_col,12+i,10).mean()
	mix_[i][3] += findMode(visualize_with_vote_or_rating_genr(m_col,12+i,10))

fig, axs1 = plt.subplots(figsize=(9, 3), sharey=True)
axs1.bar(genr, mix_[:,0])
axs1.set_title('The max amount of vote in genr')
fig, axs2 = plt.subplots(figsize=(9, 3), sharey=True)
axs2.bar(genr, mix_[:,1])
axs2.set_title('The min amount of vote in genr')
fig, axs3 = plt.subplots(figsize=(9, 3), sharey=True)
axs3.bar(genr, mix_[:,2])
axs3.set_title('The mean amount of vote in genr')
fig, axs4 = plt.subplots(figsize=(9, 3), sharey=True)
axs4.bar(genr, mix_[:,3])
axs4.set_title('The mode amount of vote in genr')
plt.show()

# visualize the rating for genr
	
m = list([6,11,17,18,22])
mix_ = np.zeros((26,4))
for i in range(26):
	if i in m:
		mix_[i][:] = 0 
		continue	
	mix_[i][0] += visualize_with_vote_or_rating_genr(m_col,12+i,5).max()
	mix_[i][1] += visualize_with_vote_or_rating_genr(m_col,12+i,5).min()
	mix_[i][2] += visualize_with_vote_or_rating_genr(m_col,12+i,5).mean()
	mix_[i][3] += findMode(visualize_with_vote_or_rating_genr(m_col,12+i,5))

fig, axs1 = plt.subplots(figsize=(9, 3), sharey=True)
axs1.bar(genr, mix_[:,0])
axs1.set_title('The max amount of rating in genr')
fig, axs2 = plt.subplots(figsize=(9, 3), sharey=True)
axs2.bar(genr, mix_[:,1])
axs2.set_title('The min amount of rating in genr')
fig, axs3 = plt.subplots(figsize=(9, 3), sharey=True)
axs3.bar(genr, mix_[:,2])
axs3.set_title('The mean amount of rating in genr')
fig, axs4 = plt.subplots(figsize=(9, 3), sharey=True)
axs4.bar(genr, mix_[:,3])
axs4.set_title('The mode amount of rating in genr')
plt.show()





