from adapters.web_scraper import AiohttpClient, BeautifulSoupParser, CourseraScraper
import aiohttp


class ScraperFactory:
    @staticmethod
    async def create_scraper() -> CourseraScraper:
        session = aiohttp.ClientSession()
        http_client = AiohttpClient(session)
        parser = BeautifulSoupParser()
        return CourseraScraper(http_client, parser)
