import json
import datetime
from pprint import pprint

#json data sanitization
tripadvisordata = json.load(open('tripadvisor.json'))

#data sanitization
for entry in tripadvisordata:
	entry["review_short"] = entry["review"][0:100]
	entry["rating"] = entry["rating"][(len(entry["rating"]))-2:(len(entry["rating"]))]

#get num reviews this week and average reviews
today = datetime.date.today()
beginDate = today - datetime.timedelta(days=7)
reviewCounter = 0
averageReviewRating = 0
tripadvisorreviews = "<ul>"

for entry in tripadvisordata:
	if (datetime.datetime.strptime(entry["date"], "%d %B %Y").date()) > beginDate:
		reviewCounter += 1
		averageReviewRating += entry["rating"]
		tripadvisorreviews += "<li>" + entry["review_short"] + "</li>"

if reviewCounter != 0:
	averageReviewRating /= reviewCounter
else: 
	tripadvisorreviews += "No reviews this week"

tripadvisorreviews += "</ul>"

#pprint(tripadvisordata)

#initalize tripadvisor mailmerge variables
print(tripadvisorreviews)

