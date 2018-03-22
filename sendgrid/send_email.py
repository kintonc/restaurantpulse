import sendgrid
import os
import datetime
import json
import time
from pprint import pprint
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


def populateRestaurants():
	#json data sanitization
	restaurantdata = json.load(open('configs/restaurants.json'))
	return restaurantdata

def datasanization_yelp(filename):
	#json data sanitization
	yelpdata = json.load(open(filename))

	#data sanitization
	for entry in yelpdata:
		entry["review_short"] = entry["review"][0:100]
		if (len(entry["review"])) > 100:
			entry["review_short"] += "..."
		entry["rating"] = entry["rating"][0:3]

		dateBeginChar = 0
		dateEndChar = 0
		for i in range(0, len(entry["date"])):
			if entry["date"][i].isdigit():
				dateBeginChar = i
				break

		for i in range(len(entry["date"]) - 1, -1, -1):
			if entry["date"][i].isdigit():
				dateEndChar = i + 1
				break

		entry["date"] = entry["date"][dateBeginChar:dateEndChar]

	#get num reviews this week and average reviews, and create yelpreviews object
	today = datetime.date.today()
	beginDate = today - datetime.timedelta(days=7)
	reviewCounter = 0
	averageReviewRating = 0
	yelpreviews = "<ul>"

	for entry in yelpdata:
		if (datetime.datetime.strptime(entry["date"], "%m/%d/%Y").date()) > beginDate:
			reviewCounter += 1
			averageReviewRating += float(entry["rating"])
			yelpreviews += "<li>" + entry["review_short"] + "</li>"

	if reviewCounter != 0:
		averageReviewRating /= reviewCounter
		averageReviewRating = round(averageReviewRating,1)
	else: 
		yelpreviews += "<li>No reviews this week</li>"
		averageReviewRating = "N/A"

	yelpreviews += "</ul>"

	returnValue = {'review': yelpreviews, 'reviewCounter': reviewCounter, 'averageReviewRating': averageReviewRating}

	#pprint(yelpdata)

	return returnValue

def datasanization_tripadvisor(filename): 
	#json data sanitization
	tripadvisordata = json.load(open(filename))

	#data sanitization
	for entry in tripadvisordata:
		entry["review_short"] = entry["review"][0:100]
		if (len(entry["review"])) > 100:
			entry["review_short"] += "..."
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
			averageReviewRating += float(entry["rating"])
			tripadvisorreviews += "<li>" + entry["review_short"] + "</li>"

	if reviewCounter != 0:
		averageReviewRating /= (reviewCounter * 10)
		averageReviewRating = round(averageReviewRating,1)
	else: 
		tripadvisorreviews += "<li>No reviews this week</li>"
		averageReviewRating = "N/A"

	tripadvisorreviews += "</ul>"

	#pprint(tripadvisordata)

	returnValue = {'review': tripadvisorreviews, 'reviewCounter': reviewCounter, 'averageReviewRating': averageReviewRating}

	return returnValue

#def run_spider(restaurantName, yelpURL, tripadvisorURL, yelpFileName, tripadvisorFileName):
	#cmdline execute from here: https://stackoverflow.com/questions/28354770/scrapy-pass-arguments-to-cmdline-execute

	#run yelp spider first
#	cmdline.execute([
#	    'scrapy', 'crawl', 'yelp', '-a', 'url='+yelpURL, 
#	    '-o', yelpFileName])
	#run tripadvisor spider
#	cmdline.execute([
#	    'scrapy', 'crawl', 'tripadvisor', '-a', 'url='+tripadvisorURL, 
#	    '-o', tripadvisorFileName])


def send_email():
	print("BEGIN send_email.py")

	#sendgrid boiler plate
	creddata = json.load(open('configs/creds.json'))
	api_key = creddata['sendgrid']
	sg = sendgrid.SendGridAPIClient(apikey=api_key)
	from_email = Email("wilburafm344@kinton.me")
	subject = "Your weekly competitor report"
	to_email = Email("kinton@kinton.me")
	content = Content("text/html", "some content")
	mail = Mail(from_email, subject, to_email, content)

	# ADD CUSTOM CONTENT

	#add date
	mail.personalizations[0].add_substitution(Substitution("-date-", \
		datetime.date.today().strftime("%B") + " " + datetime.date.today().strftime("%d") + ", " + \
		datetime.date.today().strftime("%Y")))

	#ADD REVIEW CONTENT.

	restaurants = populateRestaurants()

	#pull s3 counter number
	counterFile = open('configs/s3counter.txt', 'r')
	counter = int(counterFile.read())

	imgStyle = '"width: 100%"'
	nlpImgSrc1 = '<img src="https://s3.amazonaws.com/afm344-2/sentiment_graph_1-' + str(counter) + '.png" style=' + imgStyle + '>'
	nlpImgSrc2 = '<img src="https://s3.amazonaws.com/afm344-2/sentiment_graph_2-' + str(counter) + '.png" style=' + imgStyle + '>'
	mail.personalizations[0].add_substitution(Substitution("-nlpimage1-", nlpImgSrc1))
	mail.personalizations[0].add_substitution(Substitution("-nlpimage2-", nlpImgSrc2))


	#run this for loop X times, X being the number of restaurants we're including in our report
	for i in range(0,len(restaurants)):
		restaurantName = restaurants[str(i)]['name']
		shortName = restaurants[str(i)]['nospace_name']
		yelpURL = restaurants[str(i)]['yelp']
		tripadvisorURL = restaurants[str(i)]['tripadvisor']
		yelpFileName = '../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/' + shortName + '_yelp_' + datetime.date.today().strftime('%Y-%m-%d') + '_review.json'
		tripadvisorFileName = '../scrapy-yelp-tripadvisor/tutorial/spiders/data/json/' + shortName + '_tripadvisor_' + datetime.date.today().strftime('%Y-%m-%d') + '_review.json'
		gmapsImgSrc = '<img src="https://s3.amazonaws.com/afm344-2/traffic_' + shortName + '-' + str(counter) + '.png" style=' + imgStyle + '>'

		print("Processing data sanitization " + restaurantName + " Yelp...\n")
		yelpData = datasanization_yelp(yelpFileName)

		print("Processing data sanitization " + restaurantName + " Tripadvisor...\n")
		tripadvisorData = datasanization_tripadvisor(tripadvisorFileName)

		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "name-", restaurantName))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "yelprating-", str(yelpData['averageReviewRating'])))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "tripadvisorrating-", str(tripadvisorData["averageReviewRating"])))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "yelpreviewqty-", str(yelpData['reviewCounter'])))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "tripadvisorqty-", str(tripadvisorData['reviewCounter'])))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "yelpreviews-", yelpData['review']))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "tripadvisorreviews-", tripadvisorData['review']))
		mail.personalizations[0].add_substitution(Substitution("-r" + str(i) + "gmaps-", gmapsImgSrc))


	# htmltoinject = open('bars.html', 'r')
	#mail.personalizations[0].add_substitution(Substitution("-htmlinjection-", '<img src= \
		#"https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Official_Portrait_of_President_Donald_Trump.jpg/1200px-Official_Portrait_of_President_Donald_Trump.jpg"'))


	mail.template_id = "3e49f640-53f5-4d9c-b2ad-52d0ef931499"


	try:
	    response = sg.client.mail.send.post(request_body=mail.get())
	except urllib.HTTPError as e:
	    print (e.read())
	    exit()

	print("STATUS CODE:")
	print(response.status_code)
	print("BODY:")
	print(response.body)
	print("HEADERS:")
	print(response.headers)

send_email()
