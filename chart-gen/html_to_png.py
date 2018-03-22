import json
import requests
import base64

def html_to_image(filepath, newFileName):
	creddata = json.load(open('creds.json'))
	api_key = creddata['convertapi']
	url = 'https://v2.convertapi.com/html/to/png?Secret=' + api_key
	file = open(filepath, 'r')
	filecontent = file.read()
	filecontent = filecontent.encode("utf-8")
	filecontent_base64_encode = base64.b64encode(filecontent)

	data = {
		"Parameters": [
			{
				"Name": "File",
				"FileValue": {
					"Name": "bars.html",
					"Data": filecontent_base64_encode.decode("utf-8")
				}
			}
		]
	}

	req = requests.post(url, json=data)
	req = req.json()

	png_base64_decode = base64.b64decode(req['Files'][0]['FileData'])

	pngfile = open('../scrapy-yelp-tripadvisor/tutorial/spiders/data/png/' + newFileName + '.png', 'wb')
	pngfile.write(png_base64_decode)


filePaths = ['sentiment_graph_1', 'sentiment_graph_2', 'traffic_celebrity_hot_pot', 'traffic_hashi_izakaya', 'traffic_kinka_izakaya', 'traffic_sushi_bong', 'traffic_uncle_tetsu']

for file in filePaths:
	html_to_image(file+'.html', file)