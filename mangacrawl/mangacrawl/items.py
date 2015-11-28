# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MangaItem(scrapy.Item):

    # Manga Item Keys
    MANGA_TITLE = "title"
    MANGA_GENRE_LIST = "genre_list"
    MANGA_DATE = "date"
    MANGA_RATING_VALUE = "rating_value"
    MANGA_RATING_COUNT = "rating_count"
    MANGA_CHAPTER_COUNT = "chapter_count"
    MANGA_STATUS = "status"

    title = scrapy.Field()
    genre_list = scrapy.Field()
    date = scrapy.Field()
    rating_value = scrapy.Field()
    rating_count = scrapy.Field()
    chapter_count = scrapy.Field()
    status = scrapy.Field()

