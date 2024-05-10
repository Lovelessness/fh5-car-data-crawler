# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CardataItem(scrapy.Item):
    id = scrapy.Field()                     # 数据表内id，纯数字，为页面url中车辆id
    name = scrapy.Field()                   # 车辆实际名称
    display_name = scrapy.Field()           # 车辆显示名称，即将空格替换为&nbsp;版本
    entry_name = scrapy.Field()             # 车辆词条名称，即将空格替换为下划线版本
    alter_name = scrapy.Field()             # 车辆简称，季节赛等说明中的车辆缩略名
    display_altname = scrapy.Field()        # 车辆简称显示名称，将空格替换为&nbsp;版本
    brand = scrapy.Field()                  # 车辆制造商
    age = scrapy.Field()                    # 车辆生产年份
    nation = scrapy.Field()                 # 车辆产地的国家/地区
    type = scrapy.Field()                   # 车辆类型
    price = scrapy.Field()                  # 车辆价格
    unlock = scrapy.Field()                 # 车辆解锁方式
    rank = scrapy.Field()                   # 车辆初始性能评级
    score = scrapy.Field()                  # 车辆初始调校分数
    transmission = scrapy.Field()           # 车辆初始驱动方式
    speed = scrapy.Field()                  # 车辆初始性能参数（以下略）
    handling = scrapy.Field()
    accel = scrapy.Field()
    launch = scrapy.Field()
    braking = scrapy.Field()
    offroad = scrapy.Field()
    img_url = scrapy.Field()                # 车辆缩略图url地址
    xhh_img_id = scrapy.Field()             # 百科中缩略图id，默认为车辆id

