from web_scraper import AiohttpClient, BeautifulSoupParser, CourseraScraper
import aiohttp


class ScraperFactory:
    @staticmethod
    def create_scraper() -> CourseraScraper:
        session = aiohttp.ClientSession()
        http_client = AiohttpClient(session)
        parser = BeautifulSoupParser()
        return CourseraScraper(http_client, parser)
