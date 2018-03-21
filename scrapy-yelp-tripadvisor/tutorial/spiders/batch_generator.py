from scrapy import cmdline
import json
import datetime
import os
from pprint import pprint

def populateRestaurants():
	#json data sanitization
	restaurantdata = json.load(open('configs/restaurants.json'))
	return restaurantdata

def batch_generator():
	restaurants = populateRestaurants()

	batchscript = 'cd \"C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/scrapy-yelp-tripadvisor/tutorial/spiders"'


	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		nospace_name = restaurants[str(i)]['nospace_name']
		yelpURL = restaurants[str(i)]['yelp']
		tripadvisorURL = restaurants[str(i)]['tripadvisor']
		yelpFileName = 'json/' + nospace_name + '_yelp_' + datetime.date.today().strftime('%Y-%m-%d') + '.json'
		tripadvisorFileName = 'json/' + nospace_name + '_tripadvisor_' + datetime.date.today().strftime('%Y-%m-%d') + '.json'


		yelpCommand = 'scrapy crawl yelp -a url="' + yelpURL + '" -o "' + yelpFileName + '"'
		tripadvisorCommand = 'scrapy crawl tripadvisor -a url="' + tripadvisorURL + '" -o "' + tripadvisorFileName + '"'

		batchscript += "\n" + yelpCommand
		batchscript += "\n" + tripadvisorCommand

	batch_file = open("batchgen.bat", "w")
	batch_file.write(batchscript)
	batch_file.close()


batch_generator()