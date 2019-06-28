# -*- coding: utf-8 -*-
import scrapy


class sport_scrapper(scrapy.Spider):
    name = 'sport-xpath'
    start_urls = [
        'http://www.aljazeera.net/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'title': quote.xpath('.//small[@class="author"]/text()').extract_first()
            }

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

