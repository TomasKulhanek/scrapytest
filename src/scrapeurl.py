import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.sreality.cz/hledani/prodej/byty",
    ]
    custom_settings = {
        'DEPTH_LIMIT': 25, # 500 / 20 per page = 25
        'DOWNLOAD_DELAY': 2, 
#        'CONCURRENT_ITEMS': 1, 
#        'CONCURRENT_REQUESTS': 1        
    }

    def parse(self, response):
        for quote in response.css("div.property"):
            yield {
                "title": quote.css("span.name::text").get()+' '+quote.css("span.locality::text").get(),
                "image": quote.xpath('preact/div/div/a/img::attr("src")').get(),
                "url": quote.xpath('preact/div/div/a::attr("href")').get()
            }

        next_page = response.css('a.paging-next::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)