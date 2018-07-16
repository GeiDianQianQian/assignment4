import sys
import numpy as np
import pandas as pd
import difflib

def matchTitle(movie,movie_ratings):
    #finding similar strings
    title = difflib.get_close_matches(movie['title'], movie_ratings['title'])
    #print(title)
    copy_title = movie_ratings
    #print(copy_title)
    matched = copy_title[copy_title['title'].isin(title)]
    #print (matched)
    rating = matched['rating'].mean()
    #print(rating)
    result = round(rating,2)
    return result




def getAverageRating(movie_list,movie_ratings):
    movie_list['rating']= movie_list.apply(lambda x : matchTitle(x, movie_ratings), axis=1)
    movie_list = movie_list.dropna()
    return movie_list

def main():
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]

    list = open(file1).readlines()

    movie_list = pd.DataFrame(list, columns = ['title'])
    #print(movie_list)
    movie_ratings = pd.read_csv(file2)

    #print(movie_list)
    #print(movie_ratings['title'])
    #column_names = ['title', 'rating']
    #output = pd.DataFrame(columns = column_names)
    #print(output['rating'])

    output = getAverageRating(movie_list,movie_ratings)
    #print(output)
    output.to_csv(file3)

if __name__ == '__main__':
    main()
