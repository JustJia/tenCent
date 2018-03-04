# -*- coding: utf-8 -*-
import scrapy

from tenCent.items import TencentPlusItem


class TencentPlusSpider(scrapy.Spider):
    name = 'tencent_plus'
    allowed_domains = ['tencent.com']
    # 修改起始url
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        els = response.xpath('//*[@id="position"]/div[1]/table/tr[contains(@class,"odd") or contains(@class,"even")]')
        # els = response.xpath('//*[@id="position"]/div[1]/table/tr[position()>1 or position()<12]')
        for el in els:
            # 用构建的模板存放数据
            data_dict = TencentPlusItem()
            data_dict['name'] = el.xpath('./td[1]/a/text()')[0].extract()
            data_dict['link'] = 'https://hr.tencent.com/' + el.xpath('./td[1]/a/@href')[0].extract()
            data_dict['num'] = el.xpath('./td[3]/text()')[0].extract()
            data_dict['location'] = el.xpath('./td[4]/text()')[0].extract()
            data_dict['title'] = el.xpath('./td[2]/text()').extract_first()
            data_dict['time'] = el.xpath('./td[5]/text()')[0].extract()
            # 使用meta参数返回消息字典，meta必须是一个字典
            # 当前该信息的详细页面的请求携带meta参数，将当前页面的信息，传递到详情页面，然后跟着详情页面一起传入管道
            yield scrapy.Request(url=data_dict['link'],callback=self.parse_detail,meta={'key':data_dict})
        next_url = 'https://hr.tencent.com/' + response.xpath('//*[@id="next"]/@href').extract_first()
        if 'javascript:;' not in next_url:
            # 将next_url构造成请求然后发送给引擎，执行翻页操作
            yield scrapy.Request(url=next_url, callback=self.parse)
    # 解析详情页面函数
    def parse_detail(self,response):
        # 取出返回响应里携带的请求对象中携带的meta参数
        data_dict = response.meta['key']
        print(data_dict)
        data_dict['duty'] = ','.join(response.xpath('//tr[3]/td/ul/li/text()').extract())
        data_dict['content'] = ','.join(response.xpath('//tr[4]/td/ul/li/text()').extract())
        print('------',data_dict)
        yield data_dict