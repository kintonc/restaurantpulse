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

	batchscript = '#!/bin/sh'
	batchscript += '\ncd /home/ubuntu/afm344/scrapy-yelp-tripadvisor/tutorial/spiders'

	#scrapy commands
	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		nospace_name = restaurants[str(i)]['nospace_name']
		yelpURL = restaurants[str(i)]['yelp']
		tripadvisorURL = restaurants[str(i)]['tripadvisor']
		yelpFileName = 'data/json/' + nospace_name + '_yelp_' + datetime.date.today().strftime('%Y-%m-%d') + '_review.json'
		tripadvisorFileName = 'data/json/' + nospace_name + '_tripadvisor_' + datetime.date.today().strftime('%Y-%m-%d') + '_review.json'


		yelpCommand = 'scrapy crawl yelp -a url="' + yelpURL + '" -t json --nolog -o - > "' + yelpFileName + '"'
		tripadvisorCommand = 'scrapy crawl tripadvisor -a url="' + tripadvisorURL + '" -t json --nolog -o - > "' + tripadvisorFileName + '"'

		#batchscript += "\n" + yelpCommand
		batchscript += "\n" + tripadvisorCommand

	#gmaps scraping commands
	batchscript += '\ncd /home/ubuntu/afm344/googlemaps-foot-traffic'
	batchscript += '\npython3 gmaps_scraper.py'

	#create gmaps charts (these are in html format)
	batchscript += '\ncd /home/ubuntu/afm344/chart-gen'
	batchscript += '\npython traffic_chart.py'

	#create NLP analysis charts (these are in html format)
	batchscript += '\ncd /home/ubuntu/afm344/chart-gen'
	batchscript += '\npython NLP_analysis.py'

	#convert html charts into pngs
	batchscript += '\ncd /home/ubuntu/afm344/sendgrid'
	batchscript += '\npython html_to_image.py'

	#upload png onto S3
	batchscript += '\npython3 s3_upload.py'

	#send email python
	batchscript += '\ncd /home/ubuntu/afm344/sendgrid/'
	batchscript += '\npython send_email.py'
	batchscript += '\nexit 0'

	batch_file = open("batchgen_ubuntu.sh", "w")
	batch_file.write(batchscript)
	batch_file.close()


batch_generator()
