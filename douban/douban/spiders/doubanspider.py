#! /usr/bin/env python
# _*_ coding : utf-8 _*_

import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban.items import DoubanItem

class Douban(CrawlSpider):
	name = "douban"
	redis_key  = "douban:start_urls"
	start_urls = ["http://movie.douban.com/top250"]
	
	url = "http://movie.douban.com/top250"
	
	def parse(self,response):
		item = DoubanItem()
		selector = Selector(response)
		Movies = selector.xpath('//div[@class="info"]')
		for eachMovie in Movies:
			title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
			fulltitle = ''
			for each in title:
				fulltitle = fulltitle + each
			movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
			star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
			quote = eachMovie.xpath('div[@class="db"]/p[@class="quote"]/span/text()').extract()
			if quote:
				quote = quote[0]
			else:
				quote = ""
			item['title'] = fulltitle
			item['quote'] = quote
			item['movieInfo'] = ";".join(movieInfo)
			item['star'] = star
			yield item

		nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()
		if nextLink:
			nextLink = nextLink[0]
			print nextLink
			yield Request(self.url + nextLink,callback = self.parse)


