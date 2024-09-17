import scrapy

class AceiteOlivaSpider(scrapy.Spider):
    name = "aceite_oliva_spider"
    allowed_domains = ["juntadeandalucia.es"]
    start_urls = ["https://www.juntadeandalucia.es/agriculturaypesca/observatorio/servlet/FrontController?ec=default"]

    def parse(self, response):
            amount = response.xpath('//*[@id="myCarousel"]/div/div[1]/div[1]/a/div/div[4]/div[1]/text()').get().replace(' €', '').replace(',', '.')
            item = dict()
            item['name'] = 'ACEITE_OLIVA'
            item['price'] = str(float(amount)*100)
            item['description'] = '100'
            item['unit_measurement'] = 'L'
            yield item