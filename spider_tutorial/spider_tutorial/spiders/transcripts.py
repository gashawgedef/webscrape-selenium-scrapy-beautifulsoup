import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(
            url="https://subslikescript.com/movies",
            headers={'User-Agent': self.user_agent}
        )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    rules = (
        Rule(LinkExtractor(restrict_css="ul.scripts-list li a"), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_css="a[rel='next']"), process_request='set_user_agent'),
    )

    def parse_item(self, response):
        self.logger.info(f"Scraped URL: {response.url}")
        article = response.css('article.main-article')
        
        transcript = article.css('div.full-script *::text').getall()
        transcript_text = ' '.join(transcript).strip()
        
        yield {
            'title': article.css('h1::text').get(),
            'plot': article.css('p.plot::text').get(),
            'transcript': transcript_text,
            'url': response.url,
            'user_agent': response.request.headers['User-Agent'].decode('utf-8'),
        }
