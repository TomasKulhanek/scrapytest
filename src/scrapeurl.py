import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # "https://www.sreality.cz/hledani/prodej/byty" returns empty body, but subrequest and JS code inserts the content
    start_urls = [        
        "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=500"
    ]
    custom_settings = {
        'DEPTH_LIMIT': 1, # 500 / 20 per page = 25
        'DOWNLOAD_DELAY': 2, 
        'ROBOTSTXT_OBEY': False,
#        'CONCURRENT_ITEMS': 1, 
#        'CONCURRENT_REQUESTS': 1        
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

        #for quote in response.css("div.property"):
        #    yield {
        #        "title": quote.css("span.name::text").get()+' '+quote.css("span.locality::text").get(),
        #        "image": quote.xpath('preact/div/div/a/img::attr("src")').get(),
        #        "url": quote.xpath('preact/div/div/a::attr("href")').get()
        #    }

        #next_page = response.css('a.paging-next::attr("href")').get()
        #if next_page is not None:
        #    yield response.follow(next_page, self.parse)