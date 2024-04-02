import scrapy
from allocine.items import AllocineItem


class AllospiderSpider(scrapy.Spider):
    name = "allospider"
    allowed_domains = ["allocine.fr"]
    start_urls = ["https://www.allocine.fr/personne/top/les-plus-vues/ever/"]

    custom_settings = {
    'FEEDS' : {
        'starsdata.json' : {'format' : 'json', 'overwrite' : True},
}
}
    def parse(self, response):
        stars = response.css('div.person-card')
        for star in stars:
            relative_url = star.css('a.meta-title-link ::attr(href)').get()
            star_url = 'https://www.allocine.fr' + relative_url
            yield response.follow(star_url, callback=self.parse_star_page)

        current_page = response.meta.get('current_page', 1)
        next_page = current_page + 1

        if next_page < 21:
            next_page_url = f"https://www.allocine.fr/personne/top/les-plus-vues/ever/?page={next_page}"
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'current_page': next_page})


    def parse_star_page(self, response):
        star_item = AllocineItem()

        star_item['url'] = response.url
        star_item['name'] = response.css('div.titlebar-title-xl::text').get()
        star_item['years_career'] = response.xpath('//*[@id="content-layout"]/div[2]/div/section[1]/div/div[2]/div[1]/div[1]/text()').get()
        star_item['number_films_series'] = response.xpath('//*[@id="content-layout"]/div[2]/div/section[1]/div/div[2]/div[2]/div[1]/text()').get()

        yield star_item