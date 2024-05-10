# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import pandas
import csv


class CardataPipeline:
    def process_item(self, item, spider):
        base_dir = '车辆数据'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + '车辆数据.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if item:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'id', 'name', 'display_name', 'entry_name', 'alter_name',
                        'display_altname', 'brand', 'age', 'nation', 'type', 'price', 'unlock',
                        'rank', 'score', 'transmission',
                        'speed', 'handling', 'acceleration', 'launch', 'braking', 'offroad',
                        'img_url', 'xhh_img_id'
                    ]
                    writer.writerow(header)
                writer.writerow(
                    [item[key] for key in item.keys()])
        return item

