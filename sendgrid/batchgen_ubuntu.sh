#!/bin/sh
cd /home/ubuntu/afm344/scrapy-yelp-tripadvisor/tutorial/spiders
scrapy crawl tripadvisor -a url="https://www.tripadvisor.ca/Restaurant_Review-g155019-d4471873-Reviews-Seven_Lives-Toronto_Ontario.html#REVIEWS" -t json --nolog -o - > "data/json/sushi_bong_tripadvisor_2018-03-29_review.json"
scrapy crawl tripadvisor -a url="https://www.tripadvisor.ca/Restaurant_Review-g155019-d8277413-Reviews-Kinka_Izakaya_North_York-Toronto_Ontario.html" -t json --nolog -o - > "data/json/kinka_izakaya_tripadvisor_2018-03-29_review.json"
scrapy crawl tripadvisor -a url="https://www.tripadvisor.ca/Restaurant_Review-g155019-d10056315-Reviews-Hashi_Izakaya-Toronto_Ontario.html" -t json --nolog -o - > "data/json/hashi_izakaya_tripadvisor_2018-03-29_review.json"
scrapy crawl tripadvisor -a url="https://www.tripadvisor.ca/Restaurant_Review-g155019-d4945199-Reviews-Celebrity_Hotpot-Toronto_Ontario.html" -t json --nolog -o - > "data/json/celebrity_hot_pot_tripadvisor_2018-03-29_review.json"
scrapy crawl tripadvisor -a url="https://www.tripadvisor.ca/Restaurant_Review-g155019-d7933088-Reviews-Uncle_Tetsu_s_Cheese_Cake-Toronto_Ontario.html" -t json --nolog -o - > "data/json/uncle_tetsu_tripadvisor_2018-03-29_review.json"
cd /home/ubuntu/afm344/googlemaps-foot-traffic
python3 gmaps_scraper.py
cd /home/ubuntu/afm344/chart-gen
python traffic_chart.py
cd /home/ubuntu/afm344/chart-gen
python NLP_analysis.py
cd /home/ubuntu/afm344/sendgrid
python html_to_image.py
python3 s3_upload.py
cd /home/ubuntu/afm344/sendgrid/
python send_email.py
exit 0