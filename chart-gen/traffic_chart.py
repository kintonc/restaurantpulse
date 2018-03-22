from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import datetime
from bokeh.palettes import GnBu3, OrRd3
import json
import requests
from pprint import pprint
import os


def get_traffic_for_day(data):
    list = []
    for record in data:
        list.append(record)
    return list

def get_traffic_for_hour(data, hour):
    list = []
    for record in data:
        list.append(record['data'][hour])
    return list

def create_chart(google_data, filename, restaurant_name):
    output_file(filename+".html")

    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = ['11 am', '12 pm', '1 pm', '2 pm', '3 pm', '4 pm', '5 pm', '6 pm', '7 pm', '8 pm', '9 pm']
    populartimes = google_data[0]['populartimes']

    eleven_am = get_traffic_for_hour(populartimes, 12)
    twelve_pm = get_traffic_for_hour(populartimes, 13)
    one_pm = get_traffic_for_hour(populartimes, 14)
    two_pm = get_traffic_for_hour(populartimes, 15)
    three_pm = get_traffic_for_hour(populartimes, 16)
    four_pm = get_traffic_for_hour(populartimes, 17)
    five_pm = get_traffic_for_hour(populartimes, 18)
    six_pm = get_traffic_for_hour(populartimes, 19)
    seven_pm = get_traffic_for_hour(populartimes, 20)
    eight_pm = get_traffic_for_hour(populartimes, 21)
    nine_pm = get_traffic_for_hour(populartimes, 22)

    # pprint(eleven_am)

    data = {'weekdays': weekdays,
            '11 am': eleven_am,
            '12 pm': twelve_pm,
            '1 pm': one_pm,
            '2 pm': two_pm,
            '3 pm': three_pm,
            '4 pm': four_pm,
            '5 pm': five_pm,
            '6 pm': six_pm,
            '7 pm': seven_pm,
            '8 pm': eight_pm,
            '9 pm': nine_pm}

    x = [(weekday, hour) for weekday in weekdays for hour in hours]
    counts = sum(zip(data['11 am'], data['12 pm'], data['1 pm'], data['2 pm'], data['3 pm'], data['4 pm'], data['5 pm'],
                     data['6 pm'], data['7 pm'], data['8 pm'], data['9 pm']), ())  # like an hstack

    source = ColumnDataSource(data=dict(x=x, counts=counts))

    p = figure(x_range=FactorRange(*x), plot_height=300, plot_width=1000, title="Traffic by hour " + restaurant_name,
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0
    p.xaxis.major_label_orientation = 1.5
    p.xgrid.grid_line_color = None
    p.yaxis.visible = False

    show(p)


now = datetime.datetime.now()
date = str(now.year)+"-"+str(now.month).zfill(2)+"-"+str(now.day).zfill(2)
#date = '2018-03-21'

restaurants = ['wilbur_mexicana', 'celebrity_hot_pot', 'hashi_izakaya', 'kinka_izakaya_north_york', 'sushi_bong', 'uncle_tetsu']
#wilbur_mexicana_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[0] + "_gmaps_" + date + "_map.json"))
celebrity_hot_pot_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[1] + "_gmaps_" + date + "_map.json"))
hashi_izakaya_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[2] + "_gmaps_" + date + "_map.json"))
kinka_izakaya_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[3] + "_gmaps_" + date + "_map.json"))
sushi_bong_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[4] + "_gmaps_" + date + "_map.json"))
uncle_tetsu_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurants[5] + "_gmaps_" + date + "_map.json"))

#google_data = json.load(open('googletraffic.json'))

#create_chart(wilbur_mexicana_gmap, 'traffic_wilbur_mexicana', 'Wilbur Mexicana')
create_chart(celebrity_hot_pot_gmap, 'traffic_celebrity_hot_pot', 'Celebrity Hot Pot')
create_chart(hashi_izakaya_gmap, 'traffic_hashi_izakaya', 'Hashi  Izakaya')
create_chart(kinka_izakaya_gmap, 'traffic_kinka_izakaya', 'Kinka Izakaya')
create_chart(sushi_bong_gmap, 'traffic_sushi_bong', 'Sushi Bong')
create_chart(uncle_tetsu_gmap, 'traffic_uncle_tetsu', 'Uncle Tetsu')


