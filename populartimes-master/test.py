import populartimes 
import json


res = populartimes.get('AIzaSyDXJ4Zvd8aUqINipX9W9dPWl54DDCN0cMw', 
	['restaurant'], (43.775093, -79.413834), (43.775293, -79.413543))

print(json.dumps(res, ensure_ascii=False))

