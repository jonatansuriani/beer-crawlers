import scrapy

class BeerAdvocateSpider(scrapy.Spider):
    name = 'beeradvocate'
    allowed_domains = ['www.beeradvocate.com']
    start_urls = ['https://www.beeradvocate.com/beer/styles/']


    def parse(self, response):

        style_pages = '#ba-content li a'
        yield from response.follow_all(css=style_pages, callback=self.parse_style)

    def parse_style(self, response):
        def from_content(query):
            content_xpath = '//div[@id="ba-content"]/div[1]';
            return response.xpath(content_xpath).xpath(query).get(default='').strip()

        beers_page = response.xpath("//tr//td//a[contains(@href, '/beer/profile/')]")
        yield from response.follow_all(beers_page, callback=self.parse_beer)

        yield {
            'type' : 'style',
            'original_url': response.url,
            'doc': {
                'name': response.css('h1::text').get(),
                'description': from_content('text()'),
                'abv': from_content('span[contains(.,"ABV:")]/text()'),
                'ibu': from_content('span[contains(.,"IBU:")]/text()')
            }
        }

    def parse_beer(self, response):

        yield {
            'type' : 'beer',
            'original_url': response.url,
            'doc':{
                'name': response.css('h1::text').get(),
                'brewery': {
                    'original_url': response.urljoin(response.xpath("//dt[contains(.,'From:')]/following-sibling::dd[1]/a/@href").get()),
                    'name': response.xpath("//dt[contains(.,'From:')]/following-sibling::dd[1]/a/b/text()").get()
                }
            }
        }
        