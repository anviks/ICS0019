import os
import random
import time
import re

import scrapy


output_file = 'results.json'
if os.path.exists(output_file):
    os.remove(output_file)


class EbaySpider(scrapy.Spider):
    name = "brickset_spider"

    def start_requests(self):
        url = "https://brickset.com/sets/year-2023"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        css_selector = ".set"

        for item in response.css(css_selector):
            name_selector = './/h1/text()'
            price_selector = './/dl/dt[text()="RRP"]/following-sibling::dd/text()'
            image_selector = './/img/@src'

            if (prices := item.xpath(price_selector).extract_first()) is None:
                continue

            euro_price = re.findall(r"(?<= )[\d.]+€", prices)

            if not euro_price:
                continue

            yield {
                'Title': item.xpath(name_selector).extract_first(),
                'Price': euro_price[0],
                'Picture href': item.xpath(image_selector).extract_first()
            }

        next_page_selector = '.next a ::attr(href)'
        next_page = response.css(next_page_selector).extract_first()

        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_url, callback=self.parse)


if __name__ == '__main__':
    os.system("cd ../.. && scrapy crawl brickset_spider")
