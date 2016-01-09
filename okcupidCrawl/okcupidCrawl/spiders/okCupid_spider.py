# # -*- coding: utf-8 -*-
# __author__ = 'charlescliff'

from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class okcupidSpider(CrawlSpider):
    name = 'okcupid'
    allowed_domains = ['okcupid.com']
    login_page = "https://www.okcupid.com/login"
   # start_urls = ["http://www.linkedin.com/csearch/results?type=companies&keywords=&pplSearchOrigin=GLHD&pageKey=member-home&search=Search#facets=pplSearchOrigin%3DFCTD%26keywords%3D%26search%3DSubmit%26facet_CS%3DC%26facet_I%3D80%26openFacets%3DJO%252CN%252CCS%252CNFR%252CF%252CCCR%252CI"]
    start_urls = ["http://www.linkedin.com/csearch/results"]


    def start_requests(self):
        yield Request(url=self.login_page,callback=self.login,dont_filter=True)

  #  def init_request(self):
    #"""This function is called before crawling starts."""
  #      return Request(url=self.login_page, callback=self.login)

    def login(self, response):
    #"""Generate a login request."""
        return FormRequest.from_response(response,
            formdata={'username': 'charlie.cliff@gmail.com', 'password': 'balrog62'},
            callback=self.check_login_response)

    def check_login_response(self, response):
        self.log("-----------------------------------------")
        self.log("check_login_response")
        self.log(response.body)
        self.log("-----------------------------------------")
        if "Sign Out" in response.body:
            self.log("\n\n\nSuccessfully logged in. Let's start crawling!\n\n\n")
            # Now the crawling can begin..
            self.log('Hi, this is an item page! %s' % response.url)

            return 

        else:
            self.log("\n\n\nFailed, Bad times :(\n\n\n")



class linkdinSpider(CrawlSpider):
    name = 'linkdin'
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
   # start_urls = ["http://www.linkedin.com/csearch/results?type=companies&keywords=&pplSearchOrigin=GLHD&pageKey=member-home&search=Search#facets=pplSearchOrigin%3DFCTD%26keywords%3D%26search%3DSubmit%26facet_CS%3DC%26facet_I%3D80%26openFacets%3DJO%252CN%252CCS%252CNFR%252CF%252CCCR%252CI"]
    start_urls = ["http://www.linkedin.com/csearch/results"]


    def start_requests(self):
        yield Request(url=self.login_page,callback=self.login,dont_filter=True)

  #  def init_request(self):
    #"""This function is called before crawling starts."""
  #      return Request(url=self.login_page, callback=self.login)

    def login(self, response):
    #"""Generate a login request."""
        return FormRequest.from_response(response,
            formdata={'session_key': 'charlie.cliff@gmail.com', 'session_password': 'T3rryPr@tchet'},
            callback=self.check_login_response)

    def check_login_response(self, response):
    #"""Check the response returned by a login request to see if we aresuccessfully logged in."""
        if "Sign Out" in response.body:
            self.log("\n\n\nSuccessfully logged in. Let's start crawling!\n\n\n")
            # Now the crawling can begin..
            self.log('Hi, this is an item page! %s' % response.url)

            return 

        else:
            self.log("\n\n\nFailed, Bad times :(\n\n\n")
        # Something went wrong, we couldn't log in, so nothing happens.


    def parse_item(self, response):
        self.log("\n\n\n We got data! \n\n\n")
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ol[@id=\'result-set\']/li')
        items = []
    # for site in sites:
    #     item = LinkedconvItem()
    #     item['title'] = site.select('h2/a/text()').extract()
    #     item['link'] = site.select('h2/a/@href').extract()
    #     items.append(item)
        return items 