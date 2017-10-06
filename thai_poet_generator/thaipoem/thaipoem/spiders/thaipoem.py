import scrapy


class ThPoemSpider(scrapy.Spider):
    name = "poem"

    def start_requests(self):
        category_url = r"http://www.thaipoem.com/best/%E0%B8%81%E0%B8%A5%E0%B8%AD%E0%B8%99/%E0%B8%81%E0%B8%A5%E0%B8%AD%E0%B8%99%E0%B8%AD%E0%B8%81%E0%B8%AB%E0%B8%B1%E0%B8%81-%E0%B8%A3%E0%B8%B1%E0%B8%81%E0%B8%AB%E0%B8%A7%E0%B8%B2%E0%B8%99%E0%B8%8B%E0%B8%B6%E0%B9%89%E0%B8%87/"
        urls = [f"{category_url}{x}" for x in range(1,51)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.xpath("//a[@class='btn btn-info']/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        title = response.xpath("//div[@class='tp-content']//h1/text()").extract_first()
        name_poet = response.xpath("//div[@class='tp-content']//a[@class='font-poem-writer']/text()").extract_first()

        p1 = response.xpath("//div[@class='tp-content']//pre//text()").getall()
        poem = ''.join(p1)
        yield {
            "title": title,
            "name_poet": name_poet,
            "poem": poem,
        }
