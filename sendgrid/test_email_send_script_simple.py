import sendgrid
import os
import datetime
import json
from pprint import pprint
from sendgrid.helpers.mail import Email, Content, Substitution, Mail
try:
    # Python 3
    import urllib.request as urllib
except ImportError:
    # Python 2
    import urllib2 as urllib


#json data sanitization
yelpdata = json.load(open('yelp.json'))
pprint(data)





sg = sendgrid.SendGridAPIClient(apikey="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")
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

mail.personalizations[0].add_substitution(Substitution("-r1name-", "Sushi Bong"))
mail.personalizations[0].add_substitution(Substitution("-r1yelprating-", "4.5"))
mail.personalizations[0].add_substitution(Substitution("-r1tripadvisorrating-", "4.7"))
mail.personalizations[0].add_substitution(Substitution("-r1yelpreviews-", "<ul><li>The offering at Sushi Bong can be summed up in a few words: </li><br> \
	<li>Worst sushi I have ever had. First of all, the rice is very blant. There's no hint of vinegary or sweetness in it. I ordered a sweet potato</li><br> \
	<li>Portions are huge and fish seems very fresh! I always crave this place whenever I want to eat some</li>"))
mail.personalizations[0].add_substitution(Substitution("-r1tripadvisorreviews-", "TRIPADVISOR REVIEW The offering at Sushi Bong can be summed up in a few words: <br> \
	Worst sushi I have ever had. First of all, the rice is very blant. There's no hint of vinegary or sweetness in it. I ordered a sweet potato<br> \
	Portions are huge and fish seems very fresh! I always crave this place whenever I want to eat some"))



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
