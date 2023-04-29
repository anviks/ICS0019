import os
import random
import time

import scrapy


output_file = 'results.json'
if os.path.exists(output_file):
    os.remove(output_file)


class EbaySpider(scrapy.Spider):
    name = "ebay_spider"

    def start_requests(self):
        url = "https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        css_selector = ".s-item"

        for item in response.css(css_selector):
            name_selector = './/h3/text()'
            price_selector = './/span[@class="s-item__price"]/text()'
            image_selector = './/img/@data-src'
            yield {
                'Title': item.xpath(name_selector).extract_first(),
                'Price': item.xpath(price_selector).extract_first(),
                'Picture href': item.xpath(image_selector).extract_first()
            }

        next_page_selector = './/a[@class="pagination__next icon-link"]/@href'
        next_page = response.xpath(next_page_selector).extract_first()

        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse)


if __name__ == '__main__':
    os.system("cd ../.. && scrapy crawl ebay_spider")
