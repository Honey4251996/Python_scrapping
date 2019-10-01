import logging
import scrapy
import json
import os
from scrapy.spiders import CrawlSpider
from ..items import GsmarenaScraperItem
from scrapy.utils.project import get_project_settings

logger = logging.getLogger('logger')
settings = get_project_settings()
#API_KEY = "ca8609960d71f990311119f9c85d1a2d"

class GsmarenaSpider(CrawlSpider):
    name = 'gsmarena_spider'

    API_URL = "http://api.scraperapi.com/?api_key=%s&url=" % API_KEY
    start_urls = [
        API_URL + 'https://www.gsmarena.com/makers.php3',
        API_URL + 'https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=watch'
    ]
    base_url = 'https://www.gsmarena.com/'

    def __init__(self, *args, **kwargs):
        super(GsmarenaSpider, self).__init__(*args, **kwargs)
        self.new_products_count = 0
        logger.info(self.API_URL)

    def check_exists_product(self, url):
        data = []
        if os.path.isfile('items.json') and os.access('items.json', os.R_OK):
            # checks if file exists
            # print("File exists and is readable")
            contents = open('items.json', 'r')
            for item in contents:
                temp = json.loads(item)
                data.append(temp['url'])
                # logging.info('Json parse %s' % data)
            # products_collection = self.db[settings.get('MONGO_DATABASE')][settings.get('MONGO_COLLECTION')]
            if not url in data:
                return True
        else:
            # print("Either file is missing or is not readable, creating file...")
            return True


        return False

    def parse(self, response):
        # logging.info('Response Text %s' % response.text)
        # get phones
        links = response.xpath('//div[@class="st-text"]/table//a/@href').extract()
        brands = response.xpath('//div[@class="st-text"]/table//a/text()').extract()

        for brand, link in zip(brands, links):
            params = {'category': 'Phones', 'subcategory': brand}
            url = self.API_URL + self.base_url + link
            yield scrapy.Request(url, callback=self.parse_phone_products, meta=params)

        # get watches
        products_urls = response.xpath('//div[@id="review-body"]//a/@href').extract()
        if not products_urls:
            print("Scrap is completed!!!")
        for url in products_urls:
            params = {'category': 'Watches', 'subcategory': 'Watches'}
            url = self.base_url + url
            if self.check_exists_product(url):
                yield scrapy.Request( self.API_URL + url, callback=self.parse_product, meta=params)

    def parse_phone_products(self, response):
        products_urls = response.xpath('//div[@id="review-body"]//a/@href').extract()
        for url in products_urls:
            url = self.base_url + url
            if self.check_exists_product(url):
                yield scrapy.Request(self.API_URL + url, callback=self.parse_product, meta=response.meta)

        next_page = response.xpath('//a[@class="pages-next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(self.API_URL + self.base_url + next_page, callback=self.parse_phone_products, meta=response.meta)

    @staticmethod
    def get_info_by_name(response, name):
        return response.xpath('//tr/td/a[text()="{}"]/following::*/text()'.format(name)).extract_first()

    @staticmethod
    def get_by_data_spec(response, name):
        return ' '.join(response.xpath('//td[@data-spec="{}"]/text()'.format(name)).extract())

    def parse_product(self, response):
        self.new_products_count += 1
        item = GsmarenaScraperItem()
        item['url'] = response.url
        item['name'] = response.xpath('//h1[@data-spec="modelname"]/text()').extract_first()
        item['category'] = response.meta['category']
        item['subcategory'] = response.meta['subcategory']
        item['images'] = response.xpath('//div[@class="specs-photo-main"]/a/@href').extract()
        results = {}
        tables = response.xpath('//div[@id="specs-list"]/table')
        for table in tables:
            row_name = table.xpath('.//th[@scope="row"]/text()').extract_first()
            results[row_name] = {}
            subcats = table.xpath('.//td[@class="ttl"]/a/text()').extract()
            values = table.xpath('.//td[@class="nfo"]/text()').extract()
            for sub, val in zip(subcats, values):
                results[row_name][sub] = val

        item['data'] = results
        yield item

    def closed(self, spider):
        pass
