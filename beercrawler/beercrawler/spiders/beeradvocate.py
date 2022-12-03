import scrapy

class BeerAdvocateSpider(scrapy.Spider):
    name = 'beeradvocate'
    allowed_domains = ['www.beeradvocate.com']

    def start_requests(self):
        url = 'https://www.beeradvocate.com/beer/styles/'
        
        yield scrapy.Request(url, self.parse)

    def parse(self, response):

        style_pages = '#ba-content li a'
        yield from response.follow_all(css=style_pages, callback=self.parse_style)

    def parse_style(self, response):
        def from_content(query):
            content_xpath = '//div[@id="ba-content"]/div[1]';
            return response.xpath(content_xpath).xpath(query).get(default='').strip()

        beers_page = response.xpath("//tr//td//a[contains(@href, '/beer/profile/')][1]")
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
        brewery_url = response.urljoin(response.xpath("//dt[contains(.,'From:')]/following-sibling::dd[1]/a/@href").get())

        yield response.follow(brewery_url, callback=self.parse_brewery)

        yield {
            'type' : 'beer',
            'original_url': response.url,
            'doc':{
                'name': response.css('h1::text').get(),
                'images': response.xpath('//div[@id="main_pic_norm"]/div/img').getall(),
                'brewery': {
                    'original_url': brewery_url,
                    'name': response.xpath("//dt[contains(.,'From:')]/following-sibling::dd[1]/a/b/text()").get()
                }
            }
        }

    def parse_brewery(self, response):

        yield {
            'type' : 'brewery',
            'original_url': response.url,
            'doc':{
                'name': response.css('h1::text').get(),
                'images': response.xpath('//div[@id="main_pic_norm"]/img/@src').getall(),
                'address':{
                    'address':  response.xpath('//div[@id="info_box"]/text()').get()[2:3],
                    'zipcode':  response.xpath('//div[@id="info_box"]/text()').get()[4:5],
                    'city': response.xpath('//div[@id="info_box"]/a/text()').getall()[0],
                    'state': response.xpath('//div[@id="info_box"]/a/text()').getall()[1],
                    'country': response.xpath('//div[@id="info_box"]/a/text()').getall()[2],
                    'map': response.xpath('//div[@id="info_box"]/a/@href').getall()[3],
                    'website': response.xpath('//div[@id="info_box"]/a/@href').getall()[4]
                }
            }
        }