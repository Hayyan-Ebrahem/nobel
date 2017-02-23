#  encoding: utf-8
import re
import scrapy
import bs4
from nobel_winners.items import NWinnerBioItem

BASE_URL = 'https://en.wikipedia.org'

class WinnerBioSpider(scrapy.Spider):
    name = 'nobel_winner_bio'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    def parse(self, response):
        bs = bs4.BeautifulSoup(response.text, "lxml")
        div = bs.find(id='mw-content-text')
        for child in div.children:
            if child.name=='h2' and not child.text in ('Summary', 'See also', 'References'):
                for li in child.find_next_sibling('ol'):
                    if isinstance(li, bs4.element.Tag):
                        request = scrapy.Request(
                                BASE_URL + li.a['href'],
                                callback=self.parse_bio,
                                dont_filter=True)

                        request.meta['item'] = NWinnerBioItem()
                        yield request


    def parse_bio(self, response):
        bs = bs4.BeautifulSoup(response.text, "lxml")
        item = response.meta['item']
        img_div = bs.find('table', class_=re.compile('^infobox'))

        item['name'] = img_div.tr.th.text
        for par in img_div.findAllNext('p'):
            if par.text:
                item['mini_bio'] = par.text
            else:
                break
        # get the img link 'src'
        image_url = img_div.find("a", class_="image").find('img')['src']
        if image_url:
            # get image url 'src'
            item['image_urls'] = [''.join(['https:', image_url])]
        else:
            item['image_urls'] = []

        yield item

