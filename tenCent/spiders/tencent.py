# -*- coding: utf-8 -*-
import scrapy

from tenCent.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        els = response.xpath('//*[@id="position"]/div[1]/table/tr[contains(@class,"odd") or contains(@class,"even")]')
        # els = response.xpath('//*[@id="position"]/div[1]/table/tr[position()>1 or position()<12]')
        for el in els:
            # 用构建的模板存放数据
            data_dict = TencentItem()
            data_dict['name'] = el.xpath('./td[1]/a/text()')[0].extract()
            data_dict['link'] = 'https://hr.tencent.com/' + el.xpath('./td[1]/a/@href')[0].extract()
            data_dict['num'] = el.xpath('./td[3]/text()')[0].extract()
            data_dict['location'] = el.xpath('./td[4]/text()')[0].extract()
            data_dict['title'] = el.xpath('./td[2]/text()').extract_first()
            data_dict['time'] = el.xpath('./td[5]/text()')[0].extract()
            yield data_dict
        next_url = 'https://hr.tencent.com/' + response.xpath('//*[@id="next"]/@href').extract_first()
        if 'javascript:;' not in next_url:
            # 将next_url构造成请求然后发送给引擎，执行翻页操作
            yield scrapy.Request(url = next_url,callback=self.parse)