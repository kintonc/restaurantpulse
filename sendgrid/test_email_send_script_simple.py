import sendgrid
import os
import datetime
import json
import json
from pprint import pprint
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


def datasanization_yelp():
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

	returnValue = {'review': yelpreviews, 'reviewCounter': reviewCounter, 'averageReviewRating': averageReviewRating}

	#pprint(yelpdata)

	return returnValue

def datasanization_tripadvisor(): 
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
		averageReviewRating = "N/A"

	tripadvisorreviews += "</ul>"

	#pprint(tripadvisordata)

	returnValue = {'review': tripadvisorreviews, 'reviewCounter': reviewCounter, 'averageReviewRating': averageReviewRating}

	return returnValue



def send_email():
	creddata = json.load(open('creds.json'))
	api_key = creddata["sendgrid"]
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

	#add review content
	yelpData = datasanization_yelp()
	tripadvisorData = datasanization_tripadvisor()

	#mail.personalizations[0].add_substitution(Substitution("-r1name-", "Sushi Bong"))
	#mail.personalizations[0].add_substitution(Substitution("-r1yelprating-", str(yelpData['averageReviewRating'])))
	#mail.personalizations[0].add_substitution(Substitution("-r1tripadvisorrating-", tripadvisorData["averageReviewRating"]))
	#mail.personalizations[0].add_substitution(Substitution("-r1yelpreviews-", yelpData["review"]))
	#mail.personalizations[0].add_substitution(Substitution("-r1tripadvisorreviews-", tripadvisorData["review"]))

	mail.template_id = "efafff3d-55d1-4a76-83b1-3034477298a5"

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
