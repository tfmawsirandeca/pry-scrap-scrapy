import scrapy

class CamaronSpider(scrapy.Spider):
    name = "camaron_spider"
    allowed_domains = ["pescadosvazquez.com"]
    start_urls = ["https://pescadosvazquez.com/producto/camaron/"]

    def parse(self, response):
            item = dict()

            # Extract price values
            # Use XPath to extract the price value
            price_elements = response.xpath('//*[@id="product-593"]/div[2]/p/span[1]/bdi/text()').get().replace(' €', '').replace(',', '.')
            item['name'] = 'CAMARON'
            item['price'] = price_elements
            item['description'] = '1'
            item['unit_measurement'] = response.xpath('//*[@id="product-593"]/div[2]/p/span[3]/text()').get().replace(' ', '').replace('/', '')
            yield item