# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import SspItem
from bs4 import BeautifulSoup
import time

class SspSpiderSpider(scrapy.Spider):
    name = 'ssp_spider'
    allowed_domains = ['sspai.com']
    url = 'https://sspai.com/api/v1/articles?offset={}&limit=10&type=recommend_to_home&sort=recommend_to_home_at&include_total=false'
    start_urls =  []
    #最大页数似乎为11045
    for i in range(0,2):
        start_urls.append(url.format(i))
        # time.sleep(0.1)
        # print(start_urls)

    #start_urls = ['http://sspai.com/']



    def parse(self, response):
        # print(type(response.text))
        # print(response.text)

        j = json.loads(response.text)
        j_len = len(j['list'])
        for i in range(j_len):
            title = j['list'][i]['title']
            article_id = j['list'][i]['id']
            article_url = 'https://sspai.com/post/'+str(article_id)
            keywords = j['list'][i]['keywords']
            c_time = j['list'][i]['created_at']

            yield scrapy.Request(article_url,callback=self.article_parse,meta={'title':title,'article_id':article_id,'keywords':keywords,'c_time':c_time})
            # print(article_url)

        #pass
    def article_parse(self,response):
        title = response.meta.get('title')
        article_id = response.meta.get('article_id')
        keywords = response.meta.get('keywords')
        url = response.url
        c_time = response.meta.get('c_time')
        content = response.xpath("//div[@class='content wangEditor-txt']//text()").getall()
        # content = response.xpath("//div[@class='content wangEditor-txt']")[0].xpath('string(.)').strip()
        # print(content)
        #时间需要进一步进行清洗，如1天前，n小时前，并转换成时间格式
        article_time = response.xpath("//div[@class='actions']/time/text()").get()
        # print(article_time)
        author = response.xpath("//div[@class='user-card size60']/h4//text()").get()
        item = SspItem(title=title,article_id=article_id,url=url,content=content,article_time=article_time,author=author,keywords=keywords,c_time=c_time)
        yield item
