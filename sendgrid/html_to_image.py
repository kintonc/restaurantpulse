import requests
import json
import base64

def populateRestaurants():
	#json data sanitization
	restaurantdata = json.load(open('configs/restaurants.json'))
	return restaurantdata

def main():
	print("BEGIN html to image conversion")	
	creddata = json.load(open('configs/creds.json'))
	api_key = creddata['convertapi']
	url = 'https://v2.convertapi.com/html/to/png?Secret=' + api_key

	#PART 1 - CONVERT RESTAURANT GOOGLE MAPS GRAPHS

	restaurants = populateRestaurants()

	#run this for loop X times, X being the number of restaurants we're including in our report
	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		shortName = restaurants[str(i)]['nospace_name']

		filename = 'traffic_' + shortName
		filepath ='../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/' + filename + '.html'
		print("Converting gmaps html to png - " + restaurantName)	

		conversion(filename, filepath, url, 1030)
		#1030px is the correct width to minimize whitespace on the right hand side

	#PART 2 - CONVERT 2 SENTIMENT GRAPHS	
	for i in range(1,3):
		filename = 'sentiment_graph_' + str(i)
		filepath = '../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/' + filename + '.html'

		print("Converting html to png - sentiment_graph_" + str(i))	

		conversion(filename, filepath, url, 700)


def conversion(filename, filepath, url, width):
	file = open(filepath, 'r')
	filecontent = file.read()
	filecontent = filecontent.encode("utf-8")
	filecontent_base64_encode = base64.b64encode(filecontent)

	data = {
	    "Parameters": [
	        {
	            "Name": "File",
	            "FileValue": {
	                "Name": filename + '.html',
	                "Data": filecontent_base64_encode.decode("utf-8")
	            }
	        },
	        {
	            "Name": "ImageWidth",
	            "Value": width	
	        }
	    ]
	}

	req = requests.post(url, json=data)
	req = req.json()

	png_base64_decode = base64.b64decode(req['Files'][0]['FileData'])

	pngfile = open('../scrapy-yelp-tripadvisor/tutorial/spiders/data/png/' + filename + '.png', 'wb')
	pngfile.write(png_base64_decode)

def convertone():
	print("BEGIN html to image conversion")	
	creddata = json.load(open('configs/creds.json'))
	api_key = creddata['convertapi']
	url = 'https://v2.convertapi.com/html/to/png?Secret=' + api_key

	filename = 'sentiment_graph_1'
# gmaps:	filename = 'traffic_' + 'celebrity_hot_pot'
	filepath ='../scrapy-yelp-tripadvisor/tutorial/spiders/data/html/' + filename + '.html'
	print("Converting  html to png - " + filename)	

	conversion(filename, filepath, url, 620)


main()
#convertone()