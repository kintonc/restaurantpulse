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

		batchscript += "\n" + yelpCommand
		batchscript += "\n" + tripadvisorCommand

	#gmaps scraping commands
	batchscript += '\n cd \"C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/googlemaps-foot-traffic"'
	batchscript += '\n python gmaps_scraper.py'

	#convert html charts into pngs
	batchscript += '\n cd \"C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/sendgrid"'
	batchscript += '\n python html_to_image.py'

	#upload png onto S3
	batchscript += '\n python s3_upload.py'

	#send email python
	batchscript += '\n python send_email.py'

	batch_file = open("batchgen_windows.bat", "w")
	batch_file.write(batchscript)
	batch_file.close()


batch_generator()