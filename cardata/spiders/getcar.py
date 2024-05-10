import scrapy

from cardata.utils.translate import *
from scrapy.utils.project import get_project_settings
from cardata.items import CardataItem

import re

'''
 - age: //div[@class='title_material']/p/em  (拆分' '第一项)
 - name: //div[@class='title_material']/h1
 - alter_name: //p[@class='shortname']
 - nation: //div[@class='title_material']/p/img/@src (拆分'/'最后一项)
 - brand: //div[@class='ariane']/a[3]
 - price: //div[@class='specs']//div[@class='price']/b
 - type: //div[@class='specs']//a[@class='cty']/text()
 - score: //div[@class='car_tech']/span[1]
 - transmission: //div[@class='orig_details']/div[@class='tpw']/span[@class='transmission']
 - unlock: //div[@class='car_source']/b/text()
 - speed: //div[@class='stats_cont']/div[@class='stat speed sp']/span[@class='stat_value']
 - handling: //div[@class='stats_cont']/div[@class='stat handling']/span[@class='stat_value']
 - accel: //div[@class='stats_cont']/div[@class='stat acceleration']/span[@class='stat_value']
 - launch: //div[@class='stats_cont']/div[@class='stat launch']/span[@class='stat_value']
 - braking: //div[@class='stats_cont']/div[@class='stat braking']/span[@class='stat_value']
 - offroad: //div[@class='stats_cont']/div[@class='stat offroad']/span[@class='stat_value']
'''


class GetcarSpider(scrapy.Spider):
    name = "data"
    settings = get_project_settings()
    url_prefix = settings.get('URL_PREFIX')
    id_range = settings.get('ID_RANGE')
    img_url = settings.get('IMAGE_URL')

    def start_requests(self):
        for car_id in range(self.id_range[0], self.id_range[1]+1):
            car_info_url = self.url_prefix + str(car_id)
            yield scrapy.Request(
                url=car_info_url,
                callback=self.parse,
                meta={
                    'car_id': car_id
                }
            )

    def parse(self, response):
        data = CardataItem()
        # 获取车辆id
        car_id = response.meta.get('car_id')
        data['id'] = car_id

        # 获取车辆名称
        car_name = response.xpath('//div[@class="title_material"]/h1/text()').extract_first()
        display_name = car_name.replace(' ', '&nbsp;')
        entry_name = car_name.replace(' ', '_')
        data['name'] = car_name
        data['display_name'] = display_name
        data['entry_name'] = entry_name

        # 获取车辆简称
        alter_name = response.xpath("//p[@class='shortname']/text()").extract_first()
        data['alter_name'] = alter_name
        data['display_altname'] = alter_name.replace(' ', '&nbsp;')

        # 获取厂商
        brand = response.xpath("//div[@class='ariane']/a[3]/text()").extract_first()
        data['brand'] = brand_dict[brand] if brand_dict.get(brand) is not None else brand

        # 获取生产年份
        age = response.xpath("//div[@class='title_material']/p/em/text()").extract_first().split(' ')[0]
        data['age'] = age

        # 获取产地
        nation_en = response.xpath("//div[@class='title_material']/p/img/@src").extract_first().split('/')[-1].split('.')[0]
        nation = nation_dict[nation_en] if nation_dict.get(nation_en) is not None else nation_en
        data['nation'] = nation

        # 获取车辆类型
        car_type = response.xpath("//div[@class='specs']//a[@class='cty']/text()").extract_first()
        data['type'] = car_type

        # 获取车辆价格
        price = response.xpath("//div[@class='specs']//div[@class='price']/b/text()").extract_first()
        data['price'] = price

        # 获取解锁方式
        sources = response.xpath("//div[@class='car_source']/b/text()").extract()
        unlock = ', '.join(sources)
        data['unlock'] = unlock

        # 获取性能等级评分
        rank = response.xpath("//div[@class='car_tech']/span[1]/i/a/text()").extract_first()
        score = response.xpath("//div[@class='car_tech']/span[1]/b/text()").extract_first()
        data['rank'] = rank
        data['score'] = score

        # 获取传动方式
        transmission = response.xpath("//div[@class='tpw']/span[@class='transmission']/text()").extract_first()
        data['transmission'] = transmission + (' (' + transmission_dict[transmission] + ')') \
            if transmission_dict.get(transmission) is not None else ''

        # 获取各项性能参数
        speed = response.xpath("//div[@class='stat']/span[contains(text(),'speed')]/../span[@class='stat_value']/text()").extract_first()
        handling = response.xpath("//div[@class='stat']/span[contains(text(),'handling')]/../span[@class='stat_value']/text()").extract_first()
        accel = response.xpath("//div[@class='stat']/span[contains(text(),'Acceleration')]/../span[@class='stat_value']/text()").extract_first()
        launch = response.xpath("//div[@class='stat']/span[contains(text(),'launch')]/../span[@class='stat_value']/text()").extract_first()
        braking = response.xpath("//div[@class='stat']/span[contains(text(),'braking')]/../span[@class='stat_value']/text()").extract_first()
        offroad = response.xpath("//div[@class='stat']/span[contains(text(),'Offroad')]/../span[@class='stat_value']/text()").extract_first()
        data['speed'] = speed
        data['handling'] = handling
        data['accel'] = accel
        data['launch'] = launch
        data['braking'] = braking
        data['offroad'] = offroad

        # 获取缩略图链接
        car_id = str(car_id).zfill(3)
        data['img_url'] = re.sub(r'#id#', car_id, self.img_url)
        data['xhh_img_id'] = car_id

        print(data)
        yield data
