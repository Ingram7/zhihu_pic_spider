# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
import scrapy


class ZhihuPicPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_url_list']:
                yield scrapy.Request(url, meta={'item': item})


    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        image_name1 = item['title']
        image_name2 = request.url.split('/')[-1]
        # path = u'{}/{}'.format(item['title'], image_name)
        path = image_name1+image_name2
        return path
