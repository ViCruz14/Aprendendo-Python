import scrapy 


class OngSpider(scrapy.Spider):
    name = 'Ongs'
    start_urls = ['http://www.ongsbrasil.com.br/default.asp?Pag=52&ONG=Meio%20Ambiente&Estado=SP&cidade=S%E3o%20Paulo&PageNo=' + str(page) for page in range(1, 16)]
    

    def parse(self, response):
        links = response.xpath('//table//tr/td/div/a/@href').getall()
        for link in links:    
            final = 'http://www.ongsbrasil.com.br/' + link
            yield scrapy.Request(final, callback=self.parse_new)


    def parse_new(self, response):
        email = response.xpath('//td/input[contains(@value, "@")]/@value').get()
        nome = response.xpath('//td/span[contains(text(), "Nome")]/following::span/text()').get()
        if not nome:
            nome = response.xpath('//h1/text()').get()
        yield {'email': email, 'nome': nome}
