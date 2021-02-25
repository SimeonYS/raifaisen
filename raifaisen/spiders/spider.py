import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import RaifaisenItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class RaifaisenSpider(scrapy.Spider):
	name = 'raifaisen'
	start_urls = ['https://www.rbb.bg/bg/za-bankata/novini-analizi/novini/']

	def parse(self, response):
		post_links = response.xpath('//p/a[@class="more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_articles)

	def parse_articles(self, response):
		links = response.xpath('//div[@class="column gridModule x6 y12 z4"]/a/@href').getall()
		yield from response.follow_all(links, self.parse_post)

	def parse_post(self, response):

		date = response.xpath('//span[@class="news-title-align date"]/text()').get()
		title = response.xpath('//h1[@class="news-title-align"]/text()').get()
		content = response.xpath('//div[@class="text grid x6 y12 z4 "]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=RaifaisenItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
