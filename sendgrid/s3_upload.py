import boto
import boto.s3
import json
import os
import sys
from boto.s3.key import Key
from botocore.client import Config

def main():

	print("BEGIN s3 upload")	
	creddata = json.load(open('configs/creds.json'))
	api_key = creddata['aws_access_key_id']
	secret = creddata['aws_secret']

	#from here: https://stackoverflow.com/questions/15085864/how-to-upload-a-file-to-directory-in-s3-bucket-using-boto
	AWS_ACCESS_KEY_ID = api_key
	AWS_SECRET_ACCESS_KEY = secret
	bucket_name = 'afm344-2'
	conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(bucket_name, validate=False)
	directory = "../scrapy-yelp-tripadvisor/tutorial/spiders/data/png"

	for filename in os.listdir(directory):
		filepath = 'C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/scrapy-yelp-tripadvisor/tutorial/spiders/data/png/' + filename
		print('Uploading ' + filename + ' to Amazon S3 bucket ' + bucket_name)

		def percent_cb(complete, total):
		    sys.stdout.write('.')
		    sys.stdout.flush()


		k = Key(bucket)
		k.key = filename
		k.set_contents_from_filename(filepath,
		    cb=percent_cb, num_cb=10)

main()


