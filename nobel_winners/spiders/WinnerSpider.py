#  encoding: utf-8
import re
import scrapy
import bs4
import readability
from nobel_winners.items import NobelWinnersItem


BASE_URL = 'https://en.wikipedia.org'


def process_winner_li(li):
    winner_data = {}
    winner_data['link'] = BASE_URL + li.a['href']
    winner_data['name'], *born, winner_data['category'], winner_data['year'] = tuple(li.text.split(','))
    return winner_data


class WinnerSpider(scrapy.Spider):
    name = 'nobel_winner'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country']

    def parse(self, response):
        cleaned = readability.Document(response.text)
        bs = bs4.BeautifulSoup(cleaned)
        div = bs.find(id='mw-content-text')
        for child in div.children:
            if child.name == 'h2' and not child.text.startswith(('Summary', 'See also', 'References')):
                country = child.text.rstrip('[edit]')
                if country:
                    for li in child.find_next_sibling('ol'):
                        if type(li) is bs4.element.Tag:
                            winner_data = process_winner_li(li)
                            request = scrapy.Request(
                                winner_data['link'],
                                callback=self.parse_bio,
                                dont_filter=True)
                            request.meta['item'] = NobelWinnersItem(
                                **winner_data)
                            yield request

    def parse_bio(self, response):
        bs = bs4.BeautifulSoup(response.text)
        item = response.meta['item']
        table = bs.find('table', class_=re.compile('^infobox'))
        # bio_item['image_urls'] = image_tag['src']
        #   MAKE A CATCH AND COMPAIRE THE NAME AND THE LINK HERE
        for details in table.findAll('tr'):
            if not isinstance(details.th, bs4.element.Tag):
                continue
            if not details.th.text.lower() in ('born', 'died', 'nationality'):
                continue
                    # date_of = re.search('((\w+\s\d{1,2}[,]\s\d{4})|(\d{1,2}\s\w+\s\d{4}))', details.text)
                    # if date_of:
            item[details.th.text.lower()] = details.td.text
                    # break
        yield item
