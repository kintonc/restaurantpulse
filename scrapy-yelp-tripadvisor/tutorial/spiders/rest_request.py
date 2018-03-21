import requests
import json
import base64

#sendgrid boiler plate
creddata = json.load(open('configs/creds.json'))
api_key = creddata['convertapi']

url = 'https://v2.convertapi.com/html/to/png?Secret=' + convertapi
file = open('bars.html', 'r')
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

pngfile = open('new.png', 'wb')
pngfile.write(png_base64_decode)
