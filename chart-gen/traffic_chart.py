from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import datetime
from bokeh.palettes import GnBu3, OrRd3
import json
import requests
from pprint import pprint
import os


# Used to process gmaps json file
def get_traffic_for_hour(data, hour):
    list = []
    for record in data:
        list.append(record['data'][hour])
    return list


# Creates a bar chart
def create_chart(google_data, filename, restaurant_name):
    output_file("../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/" + filename + ".html")

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

    p = figure(x_range=FactorRange(*x), plot_height=300, plot_width=1000, title="Google Maps Hourly Traffic - " + restaurant_name,
               toolbar_location=None, tools="")

    p.vbar(x='x', top='counts', width=0.9, source=source)

    p.y_range.start = 0
    p.x_range.range_padding = 0
    p.xaxis.major_label_orientation = 1.5
    p.xgrid.grid_line_color = None
    p.yaxis.visible = False

    show(p)

print("Start traffice chart generation")

# Getting today's date to pick up today's gmaps data file
#now = datetime.datetime.now()
#date = str(now.year)+"-"+str(now.month).zfill(2)+"-"+str(now.day).zfill(2)
date = '2018-03-22'

# Picking up restaurant names to create bar chart for
#restaurants = ['wilbur_mexicana', 'celebrity_hot_pot', 'hashi_izakaya', 'kinka_izakaya', 'sushi_bong', 'uncle_tetsu']
restaurants = json.load(open('../sendgrid/configs/restaurants.json'))
restaurant_0 = restaurants['0']
restaurant_1 = restaurants['1']
restaurant_2 = restaurants['2']
restaurant_3 = restaurants['3']
restaurant_4 = restaurants['4']

# Picking up json files that contain traffic data for each restaurant
restaurant_0_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_0['nospace_name'] + "_gmaps_" + date + "_map.json"))
restaurant_1_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_1['nospace_name'] + "_gmaps_" + date + "_map.json"))
restaurant_2_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_2['nospace_name'] + "_gmaps_" + date + "_map.json"))
restaurant_3_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_3['nospace_name'] + "_gmaps_" + date + "_map.json"))
restaurant_4_gmap = json.load(open("../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/" + restaurant_4['nospace_name'] + "_gmaps_" + date + "_map.json"))

# Creating barcharts for each restaurant
create_chart(restaurant_0_gmap, 'traffic_' +  restaurant_0['nospace_name'], restaurant_0['name'])
create_chart(restaurant_1_gmap, 'traffic_' +  restaurant_1['nospace_name'], restaurant_1['name'])
create_chart(restaurant_2_gmap, 'traffic_' +  restaurant_2['nospace_name'], restaurant_2['name'])
create_chart(restaurant_3_gmap, 'traffic_' +  restaurant_3['nospace_name'], restaurant_3['name'])
create_chart(restaurant_4_gmap, 'traffic_' +  restaurant_4['nospace_name'], restaurant_4['name'])

print("End traffic chart generation")
