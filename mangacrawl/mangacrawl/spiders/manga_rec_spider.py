# -*- coding: utf-8 -*-
__author__ = 'charlescliff'

from datetime import datetime
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from mangacrawl.items import MangaItem

class myanimelistSpider(CrawlSpider):

    # 0. X Path Nodes
    NODE_STRING_TITLE = "//title/text()"
    NODE_STRING_GENRE_LIST = "//a[contains(@href,'/manga/genre/')]"
    NODE_STRING_DATE = "//span[text()='Published:']/parent::*/text()"
    NODE_STRING_RATING_VALUE = "//span[@itemprop='ratingValue']/text()"
    NODE_STRING_RATING_COUNT = "//span[@itemprop='ratingCount']/text()"
    NODE_STRING_CHAPTER_COUNT = "//span[text()='Chapters:']/parent::*/text()"
    NODE_STRING_STATUS = "//span[text()='Status:']/parent::*/text()"

    # 1. Settings
    name = "myanimelist"
    allowed_domains = ['myanimelist.net']

    # 2. Start Urls
    start_urls = [
        "http://myanimelist.net/manga/genre/1",
        "http://myanimelist.net/manga/11/Naruto"
    ]

    # 3. Rules
    rules = (
        # Parsing the
        Rule(   SgmlLinkExtractor(  allow=(r'http://myanimelist.net/manga', ),
                                    deny=('http://myanimelist.net/manga/magazine',
                                          'http://myanimelist.net/manga/genre',
                                          '/characters',
                                          '/userrecs',
                                          '/reviews',
                                          '/featured',
                                          '/stats',
                                          '/pics',
                                          '/news',
                                          '/clubs',
                                          '/forum',
                                          '/moreinfo',
                                          '/manga.php', ) ),
                callback='parse_manga_page',
                follow= False ),
    )

    # 4. Parse Functions

    @classmethod
    def parse_manga_page(cls, response):
        manga_item = MangaItem()
        
        # Title
        manga_item[MangaItem.MANGA_TITLE] = myanimelistSpider.parse_title(response)
        
        # Genre List
        genre_list = myanimelistSpider.parse_genre_list(response)
        manga_item[MangaItem.MANGA_GENRE_LIST] = genre_list

        # Publication Date
        manga_item[MangaItem.MANGA_DATE] = myanimelistSpider.parse_publication_date(response)

        # Rating Value
        try:
            manga_item[MangaItem.MANGA_RATING_VALUE] = response.xpath(myanimelistSpider.NODE_STRING_RATING_VALUE).extract()[0]
        except IndexError:
            manga_item[MangaItem.MANGA_RATING_VALUE] = 0

        # Rating Count
        try:
            manga_item[MangaItem.MANGA_RATING_COUNT] = response.xpath(myanimelistSpider.NODE_STRING_RATING_COUNT).extract()[0]
        except IndexError:
            manga_item[MangaItem.MANGA_RATING_COUNT] = 0

        # Chapter Count
        try:
            manga_item[MangaItem.MANGA_CHAPTER_COUNT] = response.xpath(myanimelistSpider.NODE_STRING_CHAPTER_COUNT).extract()[0]
        except IndexError:
            manga_item[MangaItem.MANGA_CHAPTER_COUNT] = 0

        # Status
        try:
            manga_item[MangaItem.MANGA_STATUS] = response.xpath(myanimelistSpider.NODE_STRING_STATUS).extract()[0]
        except IndexError:
            manga_item[MangaItem.MANGA_STATUS] = "Unknown"
        
        # Return
        yield manga_item

    @classmethod
    def parse_title(cls, response):
        title_string = response.xpath(myanimelistSpider.NODE_STRING_TITLE).extract()[0]
        title_string = title_string.replace('\n','')
        title_string = title_string.split('|')
        return title_string[0]

    @classmethod
    def parse_genre_list(cls, response):
        genre_list = []
        genre_nodes = response.xpath(myanimelistSpider.NODE_STRING_GENRE_LIST)
        for title in genre_nodes:
            test = title.xpath("text()").extract()[0]
            genre_list.append(test)
        return genre_list

    @classmethod
    def parse_publication_date(cls, response):
        date_string = response.xpath(myanimelistSpider.NODE_STRING_DATE).extract()[0]
        date_string = date_string.split('to')[0]
        date_string = date_string.strip()

        if date_string == 'Not available':
            publication_date = None
        else:
            try:
                publication_date = datetime.strptime(date_string, "%b  %d, %Y") 
            except ValueError:
                publication_date = datetime.strptime(date_string, "%b %Y") 
        return publication_date
