# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request
from ..items import ZhihuPicSpiderItem


class ZhihuPicSpdSpider(scrapy.Spider):
    name = 'zhihu_pic_spd'
    allowed_domains = ['zhihu.com']

    # '292901966': '有着一双大长腿是什么感觉',
    # '26297181': '大胸女生如何穿衣搭配',
    # '274143680': '男生会主动搭讪一个长得很高并且长得好看的女生吗',
    # '266695575': '当你有一双好看的腿之后会不会觉得差一张好看的脸',
    # '297715922': '有一副令人羡慕的好身材是怎样的体验',
    # '26037846': '身材好是一种怎样的体验',
    # '28997505': '有个漂亮女朋友是什么体验',
    # '29815334': '女生腿长是什么感觉',
    # '35255031': '你的身材不配你的脸是一种怎样的体验',
    # '274638737': '大胸妹子夏季如何穿搭',
    # '264568089': '你坚持健身的理由是什么现在身材怎么样敢不敢发一张照片来看看',
    # '49075464': '在知乎上爆照是一种什么样的体验',
    # '22918070': '女生如何健身练出好身材',
    # '56378769': '女生身高170cm以上是什么样的体验',
    # '22132862': '女生如何选购适合自己的泳装',
    # '46936305': '为什么包臀裙大部分人穿都不好看',
    # '266354731': '被人关注胸部是种怎样的体验',
    # '51863354': '你觉得自己身体哪个部位最漂亮',
    # '66313867': '身为真正的素颜美女是种怎样的体验',
    # '34243513': '你见过最漂亮的女生长什么样',
    # '21052148': '有哪些评价女性身材好的标准',
    # '52308383': '在校女学生如何才能穿搭得低调又时尚',
    # '50426133': '平常人可以漂亮到什么程度',
    # '268395554': '你最照骗的一张照片是什么样子',
    # '277593543': '什么时候下定决心一定要瘦的',
    # '277242822': '室友认为我的穿着很轻浮我该如何回应',
    # '36523379': '穿和服是怎样的体验'
    # '62972819': '你们见过最好看的coser长什么样'

    id_list = ['62972819','34243513','28997505']

    url = 'https://www.zhihu.com/api/v4/questions/{id}/answers?include={include}'
    include_query = 'data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&platform=desktop&sort_by=default'

    def start_requests(self):
        for id in self.id_list:
            yield Request(self.url.format(id=id, include=self.include_query),callback=self.parse)


    def parse(self, response):
        result = json.loads(response.text)
        for data in result.get('data'):
            item = ZhihuPicSpiderItem()
            item['id'] = data.get('id')
            item['voteup_count'] = data.get('voteup_count')
            item['comment_count'] = data.get('comment_count')
            item['title'] = data.get('question').get('title')

            content = data.get('content')
            if content:
                img_pattern = re.compile(r"""<img\s.*?\s?data-original\s*=\s*['|"]?([^\s'"]+).*?>""", re.I)
                image_url_list = re.findall(img_pattern, content)
                item['image_url_list'] = [ x for x in image_url_list ]
            yield item

        if 'paging' in result.keys() and result.get('paging').get('is_end') == False:
            next_page = result.get('paging').get('next')

            yield Request(next_page, self.parse)


