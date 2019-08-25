# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZhihuPicSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    voteup_count = Field()
    comment_count = Field()
    image_url_list = Field()
    title = Field()



