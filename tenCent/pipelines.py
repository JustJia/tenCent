# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from tenCent.items import TencentItem, TencentPlusItem


class TencentPipeline(object):
    def open_spider(self,spider):
        self.file=open('tencent.json','w')
    def process_item(self, item, spider):
        if isinstance(item,TencentItem):
            # 将item转换成字典
            data_dict = dict(item)
            # 将字典中的数据转换成string
            str_data = json.dumps(data_dict,ensure_ascii=False) + ';\n'
            # 写入文件
            self.file.write(str_data)
        return item
    def close_spider(self,spider):
        self.file.close()

class TencentPlusPipeline(object):
    def open_spider(self,spider):
        self.file=open('tencent1.json','w')
    def process_item(self, item, spider):
        if isinstance(item,TencentPlusItem):
            # 将item转换成字典
            data_dict = dict(item)
            # 将字典中的数据转换成string
            str_data = json.dumps(data_dict,ensure_ascii=False) + ';\n'
            # 写入文件
            self.file.write(str_data)
        return item
    def close_spider(self,spider):
        self.file.close()