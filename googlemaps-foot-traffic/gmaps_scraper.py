import populartimes 
import json
import datetime

def populateRestaurants():
	#json data sanitization
	restaurantdata = json.load(open('../sendgrid/configs/restaurants.json'))
	return restaurantdata

def gmapsscraping():
	print("BEGIN google maps scraping")
	creddata = json.load(open('../sendgrid/configs/creds.json'))
	api_key = creddata['gmaps']

	restaurants = populateRestaurants()

	#run this for loop X times, X being the number of restaurants we're including in our report
	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		shortName = restaurants[str(i)]['nospace_name']
		minLat = restaurants[str(i)]['minlat']
		minLon = restaurants[str(i)]['minlon']
		maxLat = restaurants[str(i)]['maxlat']
		maxLon = restaurants[str(i)]['maxlon']

		print("Processing gmaps scraping " + restaurantName + " ...\n")

		res = populartimes.get(api_key, 
			['restaurant'], (minLat, minLon), (maxLat, maxLon))

		filename ='../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/' + shortName + '_gmaps_' + datetime.date.today().strftime('%Y-%m-%d') + '.json'

		newfile = open(filename, 'w')
		newfile.write(json.dumps(res, ensure_ascii=False))
		newfile.close()

	print("END gmaps scraping")

gmapsscraping()