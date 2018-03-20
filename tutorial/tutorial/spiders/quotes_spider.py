import scrapy


class QuotesSpider(scrapy.Spider):
    # "name" identifies our spider
    name = "yelp"

    #must return an iterable of Requests (you can return a list of requests or 
    #write a generator function) which the Spider will begin to crawl from. 
    #Subsequent requests will be generated successively from these initial 
    #requests
    def start_requests(self):
        urls = [
            'https://www.yelp.com/biz/sushi-bong-markham?sort_by=date_desc&start=0',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    #parse: a method that will be called to handle the response downloaded 
    #for each of the requests made
    #The response parameter is an instance of TextResponse that holds the 
    #page content and has further helpful methods to handle it.

    #The parse() method usually parses the response, extracting the scraped data 
    #as dicts and also finding new URLs to follow and creating new requests (Request) 
    #from them.
    def parse(self, response):
        for review in response.css("div.review-content"):
            yield {
                'date': review.css('div.biz-rating.biz-rating-large.clearfix span.rating-qualifier::text')[0].extract(),
                'rating': review.css('div.biz-rating.biz-rating-large.clearfix div.i-stars::attr(title)')[0].extract(),
                'review': review.css('div.review-content p::text')[0].extract(),
            }

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)



class TripAdvisorSpider(scrapy.Spider):
    # "name" identifies our spider
    name = "tripadvisor"

    #must return an iterable of Requests (you can return a list of requests or 
    #write a generator function) which the Spider will begin to crawl from. 
    #Subsequent requests will be generated successively from these initial 
    #requests
    def start_requests(self):
        urls = [
            'https://www.tripadvisor.ca/Restaurant_Review-g155019-d4471873-Reviews-Seven_Lives-Toronto_Ontario.html#REVIEWS',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    #parse: a method that will be called to handle the response downloaded 
    #for each of the requests made
    #The response parameter is an instance of TextResponse that holds the 
    #page content and has further helpful methods to handle it.

    #The parse() method usually parses the response, extracting the scraped data 
    #as dicts and also finding new URLs to follow and creating new requests (Request) 
    #from them.
    def parse(self, response):
        for review in response.css("div.review-container div.innerBubble > div.wrap"):
            yield {
                'date': review.css('div.rating.reviewItemInline > span[class^=\"ratingDate\"]::attr(title)').extract_first(),
                'rating': review.css('div.rating.reviewItemInline > span[class^=\"ui_bubble\"]::attr(class)').extract_first(),
                'title': review.css('div.review-container div.innerBubble > div.wrap div.quote span.noQuotes::text').extract_first(),
                'review': review.css('div.prw_rup.prw_reviews_text_summary_hsx p.partial_entry::text').extract_first(),
            }

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
