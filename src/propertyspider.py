"""
Spider of SCRAPY framework, gets properties from external URL and extract only data that is relevant for our app
"""
import scrapy

class PropertySpider(scrapy.Spider):
    name = "quotes"
    # "https://www.sreality.cz/hledani/prodej/byty" returns empty body, but subrequest and JS code inserts the content from api
    start_urls = [        
        "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500"
    ]
    custom_settings = {
        'DEPTH_LIMIT': 1, # just this api call - no subsequent is needed
        'DOWNLOAD_DELAY': 2, 
        'ROBOTSTXT_OBEY': False, # robots.txt disallows to crawl - obey for testing purpose, for production need to register into sreality developer programme
    }
    test_url_prefix = "https://www.sreality.cz/api"
    def parse(self, response):
        jsonresponse = response.json()
        # estates = jsonresponse._embedded.estates
        for estate in jsonresponse['_embedded']['estates']:
            yield {
                "title": estate['name']+" "+estate['locality'],
                "image": estate['_links']['images'][0]['href'],
                "url": self.test_url_prefix+estate['_links']['self']['href']
            }
