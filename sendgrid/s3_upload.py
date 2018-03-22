import boto
import boto3
import boto.s3
import json
import os
import sys
from boto.s3.key import Key

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

	#we need to keep a counter in order to ensure that we are not uploading files with the
	#same file name onto s3
	#so file names on s3 will be: traffic-kinkaku-1.png, traffic-kinkaku-2.png, etc
	#we keep this counter in  s3counter.txt
	counterFile = open('configs/s3counter.txt', 'r')
	counter = counterFile.read()
	print(counter)
	counter = int(counter)
	counter += 1

	for filename in os.listdir(directory):		
		#windows 
		#filepath = 'C:/Users/kinto/Dropbox/1-Waterloo/AFM 344/Final project/afm344/scrapy-yelp-tripadvisor/tutorial/spiders/data/png/' + filename
		#ubuntu 
		filepath = '/home/ubuntu/afm344/scrapy-yelp-tripadvisor/tutorial/spiders/data/png/' + filename
		s3FileName = filename[0:len(filename)-4] + '-' + str(counter) + '.png'

		print('Uploading ' + filename + ' to Amazon S3 bucket ' + bucket_name + ', S3 filename: ' + s3FileName)

		def percent_cb(complete, total):
		    sys.stdout.write('.')
		    sys.stdout.flush()


		k = Key(bucket)
		k.key = s3FileName #here, we set the name of the S3 file
		k.set_contents_from_filename(filepath, #here, we point to where the file is sitting locally
		    cb=percent_cb, num_cb=10)

	counterFile = open('configs/s3counter.txt', 'w')
	counterFile.write(str(counter))	
	counterFile.close()

main()


