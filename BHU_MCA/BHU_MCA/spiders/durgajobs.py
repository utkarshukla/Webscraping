# -*- coding: utf-8 -*-
import scrapy


class DurgajobsSpider(scrapy.Spider):
    name = 'durgajobs'
    allowed_domains = ['durgajobs.com']
    start_urls = ['http://durgajobs.com/']

    def parse(self, response):
        pass
