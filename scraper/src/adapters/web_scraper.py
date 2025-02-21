from bs4 import BeautifulSoup
from model.courses import Course
import re
from typing import AsyncGenerator, Protocol
import aiohttp
import asyncio


class HttpClient(Protocol):
    async def get(self, url: str) -> str:
        ...

class Parser(Protocol):
    def parse(self, content: str) -> BeautifulSoup:
        ...

class Scraper(Protocol):
    async def scrape_courses(self) -> AsyncGenerator['Course', None]:
        ...


class AiohttpClient:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def get(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

class BeautifulSoupParser:
    def parse(self, content: str) -> BeautifulSoup:
        return BeautifulSoup(content, "html.parser")
    

class CourseraScraper:
    def __init__(
        self, 
        http_client: HttpClient,
        parser: Parser,
        base_url: str = "https://www.coursera.org"
    ):
        self.http_client = http_client
        self.parser = parser
        self.base_url = base_url

    async def _extract_course_details(self, li_element: BeautifulSoup) -> Course:
        course_name = li_element.find(
            "h3", class_="cds-CommonCard-title css-6ecy9b"
        ).text.strip()

        try:
            img_tag = (
                li_element.find("div", class_="cds-ProductCard-gridPreviewContainer")
                .find("div", class_="cds-CommonCard-previewImage")
                .find("img")
            )
            image_url = img_tag["src"].split("?")[0]
        except AttributeError:
            image_url = ""

        url_course = self.base_url + li_element.find("div", class_="cds-ProductCard-header").find("a")["href"]
        
        course_content = await self.http_client.get(url_course)
        course_soup = self.parser.parse(course_content)

        return Course(
            name=course_name,
            tags=self._extract_tags(course_soup),
            difficulty=self._extract_difficulty(li_element),
            instructor_name=self._extract_instructor(course_soup),
            url=url_course,
            summary=self._extract_summary(course_soup),
            description=self._extract_description(course_soup),
            reviews=self._extract_reviews(course_soup),
            duration=self._extract_duration(course_soup),
            enrolled=self._extract_enrolled(course_soup),
            rating=self._extract_rating(course_soup),
            language=self._extract_language(course_soup),
            price=self._extract_price(course_soup),
            image_url=image_url
        )


    def _extract_tags(self, soup: BeautifulSoup) -> str | None:
        try:
            tags_list = soup.find_all("span", class_="css-1l1jvyr")
            return "\n".join([item.text for item in tags_list])
        except:
            return None


    def _extract_difficulty(self, li: BeautifulSoup) -> str | None:
        try:
            return li.find("div", class_="cds-ProductCard-footer").find("p", class_="css-vac8rf").text.split(" ")[0]
        except AttributeError:
            return None
        

    def _extract_instructor(self, soup: BeautifulSoup) -> str | None:
        instructor_name = soup.select_one(
            "#rendered-content > div > main > section:nth-of-type(2) > div > div > div:first-of-type "
            "> div:first-of-type > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div "
            "> div:nth-of-type(2) > div:first-of-type > p > span > a",
        )
        if instructor_name:
            return instructor_name.text.strip()
        else:
            return None
        

    def _extract_summary(self, soup: BeautifulSoup) -> str:
        try:
            summary = (
                soup.find("div", class_="css-12wvpfc")
                .find("p", class_="css-4s48ix")
                .text
            )
        except AttributeError:
            summary = ""

        return summary


    def _extract_description(self, soup: BeautifulSoup) -> str | None:
        try:
            description = ""
            description_list = soup.find_all(
                "li", class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64"
            )
            description = "\n".join([item.text for item in description_list])

        except AttributeError as e:
            description = None

        return description
    

    def _extract_reviews(self, soup: BeautifulSoup) -> str | None:
        try:
            reviews = soup.find("p", class_="css-vac8rf").text
            match = re.search(r"\b(\d{1,3}(?:,\d{3})*\b)", reviews)
            reviews_number_str = match.group(1)
            reviews = int(reviews_number_str.replace(",", ""))
        except AttributeError:
            reviews = 0

        return reviews
    

    def _extract_duration(self, soup: BeautifulSoup) -> str | None:
        try:
            duration_string = (
                soup.find_all("div", class_="css-dwgey1")[3]
                .find("div", class_="css-fw9ih3")
                .find("div")
                .text
            )
        except AttributeError:
            duration_string = None

        return duration_string
    

    def _extract_enrolled(self, soup: BeautifulSoup) -> str:
        try:
            enrolled = soup.select_one(
                "#rendered-content > div > main > section:nth-of-type(2) > div > div > div:first-of-type "
                "> div:first-of-type > div > div > div:nth-of-type(2) > div:nth-of-type(4) > p > span > strong > span"
            ).text
            enrolled = int(enrolled.replace(",", ""))
        except AttributeError:
            enrolled = 0

        return enrolled
    

    def _extract_rating(self, soup: BeautifulSoup) -> str | None:
        try:
            rating = soup.find(
                "div", class_="cds-119 cds-Typography-base css-h1jogs cds-121"
            ).text
            rating = float(rating)
        except AttributeError:
            rating = None

        return rating
    

    def _extract_language(self, soup: BeautifulSoup) -> str:
        try:
            language = soup.select_one(
                "#about > div > div:nth-of-type(3) > div:nth-of-type(2) > div:nth-of-type(2) > div:first-of-type > span"
            ).text
            language = language.replace("Taught in ", "")
        except AttributeError:
            language = "English"

        return language
    

    def _extract_price(self, soup: BeautifulSoup) -> str | None:
        try:
            price = soup.select_one(
                '[data-test="enroll-button-label"]'
            ).text.strip()
        except AttributeError:
            price = None

        return price


    async def _scrape_page(self, page_number: int) -> AsyncGenerator[Course, None]:
        url = f"{self.base_url}/courses?page={page_number}&index=prod_all_products_term_optimization"
        
        try:
            content = await self.http_client.get(url)
            soup = self.parser.parse(content)
            li_elements = soup.find_all("li", class_="cds-9")

            tasks = [self._extract_course_details(li) for li in li_elements]
            for task in asyncio.as_completed(tasks):
                try:
                    course = await task
                    yield course
                except Exception as e:
                    print(f"Error processing course: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error processing page {page_number}: {str(e)}")

    async def scrape_courses(self) -> AsyncGenerator[Course, None]:
        for page in range(1, 10):
            async for course in self._scrape_page(page):
                yield course
