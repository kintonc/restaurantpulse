import json
from pprint import pprint

#json data sanitization
yelpdata = json.load(open('yelp.json'))

yelpreviews = "<ul>"


#data sanitization
for entry in yelpdata:
	entry["review_short"] = entry["review"][0:100]
	entry["rating"] = entry["rating"][0:3]

#get num reviews this week and average reviews
for entry in yelpdata:
	beginDate = 
	if (entry["date"])
	entry["review_short"] = entry["review"][0:100]
	entry["rating"] = entry["rating"][0:3]


#create yelpreviews object
yelpreviews = "<ul>"
for entry in yelpdata:
	yelpreviews += "<li>" + entry["review_short"] + "</li>"
yelpreviews += "</ul>"

#pprint(yelpdata)

#initalize yelp mailmerge variables
print(yelpreviews)

