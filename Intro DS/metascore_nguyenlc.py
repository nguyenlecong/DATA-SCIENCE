import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('imdbdata/dataset.csv', header = 0, sep = ',')

metascore = df.iloc[:, 6].dropna()

def values():
    """ max, min, mean, mode """

    max_val = metascore.max()
    min_val = metascore.min()
    mean_val  = metascore.mean()
    mode_val = metascore.mode()
    print('min: ', min_val, 'max: ', max_val, 'mean: ', mean_val, 'mode', mode_val)

def film_count_by_metascore():
    """ Số phim theo điểm số """
    meta_score = {'quá tệ': 0, 'không hay': 0, 'bình thường': 0, 'khá hay': 0, 'rất hay': 0}

    for i in metascore:
        if i in range(0,20):
            meta_score['quá tệ'] += 1
        elif i in range(20,40):
            meta_score['không hay'] += 1
        elif i in range(40,61):
            meta_score['bình thường'] += 1
        elif i in range(61,81):
            meta_score['khá hay'] += 1
        elif i in range(81,101):
            meta_score['rất hay'] += 1

    print(meta_score)

    keys_m = meta_score.keys()
    vals_m = meta_score.values()

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}% ({v:d})'.format(p=pct,v=val)
        return my_autopct

    plt.pie(vals_m, labels = keys_m, autopct=make_autopct(vals_m))
    plt.show()

    return keys_m, vals_m

def film_count_by_metascoreNrating(keys_m, vals_m):
    """ Số phim theo điểm số của metascore và rating """

    rating = df.iloc[:, 5].dropna()
    print(rating)

    ratings = {'quá tệ': 0, 'không hay': 0, 'bình thường': 0, 'khá hay': 0, 'rất hay': 0}

    for i in rating:
        if i >= 0 and i < 2:
            ratings['quá tệ'] += 1
        elif i >= 2 and i < 4:
            ratings['không hay'] += 1
        elif i >= 4 and i <= 6:
            ratings['bình thường'] += 1
        elif i > 6 and i <= 8:
            ratings['khá hay'] += 1
        elif i > 8 and i <= 10:
            ratings['rất hay'] += 1

    print(ratings)

    keys_r = ratings.keys()
    vals_r = ratings.values()

    plt.subplot(1,2,1)
    plt.bar(keys_m, vals_m)
    plt.ylabel('Number of movies')
    plt.title('Metascore')

    plt.subplot(1,2,2)
    plt.bar(keys_r, vals_r)
    plt.ylabel('Number of movies')
    plt.title('Rating')
    plt.show()

def mean_metascore_of_genre():
    """ Điểm số trung bình của các thể loại phim """

    genres = {'Action': 0, 'Adventure': 0, 'Animation': 0, 'Biography': 0, 'Comedy':0,\
            'Crime': 0, 'Documentary': 0, 'Drama': 0, 'Family': 0, 'Fantasy': 0, 'Film-Noir':0,\
            'Game-Show': 0, 'History': 0, 'Horror': 0, 'Music': 0, 'Musical': 0, 'Mystery': 0,\
            'News': 0, 'Reality-TV': 0, 'Romance': 0, 'Sci-Fi': 0, 'Sport': 0, 'Talk-Show': 0,\
            'Thriller': 0, 'War': 0, 'Western': 0}

    genre = df.iloc[:, 12:38]
    metascore_ = df.iloc[:,6]
    gen_met = pd.concat([genre, metascore_], axis=1, sort=False)
    gen_met = gen_met.dropna()

    val_meta = []

    for i in range(len(genre.columns)):
        val = 0
        count = 0
        for index, j in gen_met.iloc[:, i].items():    
            if j == 1:
                val += metascore[index]
                count += 1
            
        if count !=0:
            val /= count
        val_meta.append(val)

    max_meta = max(val_meta)
    min_meta = min(val_meta)

    for i,x in enumerate(val_meta):
        if x == max_meta:
            print('max metascore: ', max_meta, '- of genres: ', list(genres.keys())[i])
        if x == min_meta:
            print('min metascore: ', min_meta, '- of genres: ', list(genres.keys())[i])

    for i in genres:
        index_ = list(genres.keys()).index(i)
        genres[i] = val_meta[index_]


    keys_vm = genres.keys()
    vals_vm = genres.values()

    per = np.arange(len(keys_vm))
    plt.barh(per, vals_vm)
    plt.yticks(per, keys_vm)
    plt.xlabel('Medium of metascore')
    plt.show()

    return genre, gen_met, keys_vm

def very_good_film_per_each_genre(genre, gen_met,keys_vm):
    """Số lượng phim có điểm số > 80 (phim rất hay) với mỗi thể loại"""
    good = []
    for i in range(len(genre.columns)):
        val = 0
        count = 0
        for index, j in gen_met.iloc[:, i].items():    
            if j == 1 and metascore[index] > 80:
                count += 1
        good.append(count)

    per = np.arange(len(keys_vm))
    plt.barh(per, good)
    plt.yticks(per, keys_vm)
    plt.xlabel('Numbers of film has metascore > 80 with each genre')
    plt.show()

if __name__ == "__main__":
    values()
    key,val =  film_count_by_metascore()
    film_count_by_metascoreNrating(key,val)
    genre, gen_met, keys_vm = mean_metascore_of_genre()
    very_good_film_per_each_genre(genre, gen_met,keys_vm)