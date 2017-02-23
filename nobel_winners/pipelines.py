import scrapy
from scrapy.pipelines.images import ImagesPipeline

class NobelWinnersPipeline(object):
    def process_item(self, item, spider):
        print (spider.name)
        if spider.name not in ('nobel_winner'):
            return item


class NobelImagesPipeline(ImagesPipeline):

    # def process_item(self, item, spider):
    #     if spider.name not in ['nwinners_minibio']:
    #         return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths

        return item
