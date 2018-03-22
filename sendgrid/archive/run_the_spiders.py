from scrapy import cmdline
import json
import datetime
import os
from pprint import pprint

def populateRestaurants():
	#json data sanitization
	restaurantdata = json.load(open('configs/restaurants.json'))
	return restaurantdata

def run_the_spider():
	restaurants = populateRestaurants()


	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		nospace_name = restaurants[str(i)]['nospace_name']
		yelpURL = restaurants[str(i)]['yelp']
		tripadvisorURL = restaurants[str(i)]['tripadvisor']
		yelpFileName = 'json/' + nospace_name + '_yelp_' + datetime.date.today().strftime('%Y-%m-%d') + '.json'
		tripadvisorFileName = 'json/' + nospace_name + '_tripadvisor_' + datetime.date.today().strftime('%Y-%m-%d') + '.json'

		yelpCommand = 'scrapy crawl yelp -a url=' + yelpURL + ' -o ' + yelpFileName
		tripadvisorCommand = 'scrapy crawl tripadvisor -a url=' + tripadvisorURL + ' -o ' + tripadvisorFileName


		print(yelpCommand)
		#print(tripadvisorCommand)

#scrapy crawl yelp -o "json/sushi_bong_yelp_2018-03-21.json"

#scrapy crawl yelp -a url="https://www.yelp.com/biz/sushi-bong-markham?sort_by=date_desc&start=0" -o "json/sushi_bong_yelp_2018-03-21.json"

#		os.system('cd C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/scrapy-yelp-tripadvisor/tutorial/spiders')
#		os.system(yelpCommand)
#		os.system(tripadvisorCommand)

		#cmdline execute from here: https://stackoverflow.com/questions/28354770/scrapy-pass-arguments-to-cmdline-execute
		#cmdline.execute([
		 #   'scrapy', 'crawl', 'yelp', '-a', 'url='+yelpURL, 
		  #  '-o', yelpFileName])

#		cmdline.execute([
#		    'scrapy', 'crawl', 'tripadvisor', '-a', 'url='+tripadvisorURL, 
#		    '-o', tripadvisorFileName])

run_the_spider()