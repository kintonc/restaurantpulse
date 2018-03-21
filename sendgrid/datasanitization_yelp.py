import json
import datetime
from pprint import pprint

#json data sanitization
yelpdata = json.load(open('yelp.json'))

#data sanitization
for entry in yelpdata:
	entry["review_short"] = entry["review"][0:100]
	entry["rating"] = entry["rating"][0:3]
	entry["date"] = entry["date"][9:(len(entry["date"])-5)]

#get num reviews this week and average reviews, and create yelpreviews object
today = datetime.date.today()
beginDate = today - datetime.timedelta(days=7)
reviewCounter = 0
averageReviewRating = 0
yelpreviews = "<ul>"


for entry in yelpdata:
	if (datetime.datetime.strptime(entry["date"], "%m/%d/%Y").date()) > beginDate:
		reviewCounter += 1
		averageReviewRating += entry["rating"]
		yelpreviews += "<li>" + entry["review_short"] + "</li>"

if reviewCounter != 0:
	averageReviewRating /= reviewCounter
else: 
	yelpreviews += "No reviews this week"

yelpreviews += "</ul>"

#pprint(yelpdata)

#initalize yelp mailmerge variables
print(yelpreviews)

