import scrapy
from dpst.items import DpstItem


class stdpSpider(scrapy.Spider):
    name = 'stdp'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?term=инди&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search/?term=инди&supportedlang=russian&page=2&ndl=1',
        'https://store.steampowered.com/search/?term=стратегии&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search/?term=стратегии&supportedlang=russian&page=2&ndl=1',
        'https://store.steampowered.com/search/?term=minecraft&supportedlang=russian&page=1&ndl=1',
        'https://store.steampowered.com/search/?term=minecraft&supportedlang=russian&page=2&ndl=1']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        games = response.xpath('//@href').extract()
        for game in games:
            if len(game) >= 34 and game[:34] == 'https://store.steampowered.com/app':
                yield scrapy.Request(url=game, callback=self.parse_games)

    def parse_games(self, response):

        items = DpstItem()

        items['name'] = response.css('div.apphub_AppName::text').get()
        items['category'] = response.xpath('//div[@class="blockbg"]//text()').extract()[1::2][1:-1]
        items['n_reviews'] = response.css('meta[itemprop="reviewCount"]').attrib['content']
        score = response.xpath(
          '//div[@class="summary column"]//span[@class="game_review_summary positive"]//text()').extract()[0]
        items['date'] = response.css('div.date::text').get()
        items['dev'] = response.xpath('//div[@id="developers_list"]//text()').extract()[1]
        tags = response.xpath('//a[@class="app_tag"]//text()').extract()
        price = response.xpath('//div[@class="game_purchase_price price"]/text()')[0].extract()
        platforms = response.xpath('//div[@class="sysreq_tabs"]//text()').extract()

        for i in range(len(tags)):
            tags[i] = tags[i].strip()
        items['tags'] = tags

        for i in range(len(platforms)):
            platforms[i] = platforms[i].strip()
        platforms = [x for x in platforms if x != '']

        items['platforms'] = platforms
        items['price'] = ''.join(price).strip()
        yield items
