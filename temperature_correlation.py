import sys
import numpy as np
import pandas as pd
import gzip
import matplotlib.pyplot as plt
from math import sqrt, cos, asin

#Quotation: https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
def haversine(lat1, lon1, lat2, lon2):
    p = np.pi/180     #Pi/180
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a)) * 1000 #2*R*asin...

def distance(city, stations):
    #stations['distance'] = stations.apply(lambda x: haversine(city['latitude'], city['longitude'], x['latitude'], x['longitude']), axis=1)
    stations['distance'] = np.vectorize(haversine)(city['latitude'], city['longitude'], stations['latitude'], stations['longitude'])
    #print(stations['distance'])
    return stations


def best_tmax(city,stations):
    station_distance = distance(city,stations)
    #print(station_distance)
    number = np.argmin(station_distance['distance'])
    #print('number',number)
    best_value = stations['avg_tmax'].iloc[number]
    #print('best_value',best_value)
    return best_value

def apply(citys, stations):
    citys['avg_tmax'] = citys.apply(lambda x: best_tmax(x, stations),axis=1 )
    #print(citys['avg_tmax'])
    return citys



def main():
    #read files
    stations_filename = sys.argv[1]
    citys_filename = sys.argv[2]
    output_filename = sys.argv[3]

    station_fh = gzip.open(stations_filename, 'rt', encoding='utf-8')
    stations = pd.read_json(station_fh, lines=True)
    citys = pd.read_csv(citys_filename)
    #print(stations.head())
    #print(citys.head())
    #print(citys[:1])

    #deal with data
    stations['avg_tmax'] = stations['avg_tmax']/10;
    citys = citys.dropna()
    citys['area'] = citys['area']/1000000
    citys = citys[citys['area'] <= 10000] #remove lines324, 546
    citys['density'] = citys['population'] / citys['area']
    #print(stations.head())
    #print(citys[:1]) #total is 339 rows


    #distance(citys[:1], stations)
    #best_tmax(citys[:1], stations)

    citys = apply(citys,stations)
    plt.xlabel('Avg Max Temperature (\u00b0C)')
    plt.ylabel('Population Density (people/km\u00b2)')
    plt.title('Temperature vs Population Density')
    plt.scatter(citys['avg_tmax'],citys['density'])
    #plt.show()
    #plt.savefig('output.svg')
    plt.savefig(output_filename)
    #output.to_csv(output_filename)

if __name__ == '__main__':
    main()
