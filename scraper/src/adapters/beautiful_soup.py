from bs4 import BeautifulSoup
from model.courses import Course
import requests
import re

COURSERA_URL = "https://www.coursera.org"


class WebScraper:
    def generate_scraped_courses():
        raise NotImplementedError("Subclasses must implement this method.")


class BeatifulSoupScraper(WebScraper):
    @staticmethod
    def _scrape_course_details(li):
        course_name = li.find(
            "h3", class_="cds-CommonCard-title css-6ecy9b"
        ).text.strip()

        try:
            img_tag = (
                li.find("div", class_="cds-ProductCard-gridPreviewContainer")
                .find("div", class_="cds-CommonCard-previewImage")
                .find("img")
            )
            image_url = img_tag["src"]
            image_url = image_url.split("?")[0]
        except AttributeError as e:
            image_url = ""

        try:
            difficulty = (
                li.find("div", class_="cds-ProductCard-footer")
                .find("p", class_="css-vac8rf")
                .text
            )
            difficulty = difficulty.split(" ")[0]
        except AttributeError:
            difficulty = ""

        url_course = li.find("div", class_="cds-ProductCard-header").find("a")["href"]
        url_course = COURSERA_URL + url_course
        page_course = requests.get(url_course)

        soup_course = BeautifulSoup(page_course.content, "html.parser")

        try:
            tags = ""
            tags_list = soup_course.find_all("span", class_="css-1l1jvyr")
            tags = "\n".join([item.text for item in tags_list])

        except:
            tags = None

        try:
            rating = soup_course.find(
                "div", class_="cds-119 cds-Typography-base css-h1jogs cds-121"
            ).text
            rating = float(rating)
        except AttributeError:
            rating = None

        try:
            reviews = soup_course.find("p", class_="css-vac8rf").text
            match = re.search(r"\b(\d{1,3}(?:,\d{3})*\b)", reviews)
            reviews_number_str = match.group(1)
            reviews = int(reviews_number_str.replace(",", ""))
        except AttributeError:
            reviews = 0

        try:
            duration_string = (
                soup_course.find_all("div", class_="css-dwgey1")[3]
                .find("div", class_="css-fw9ih3")
                .find("div")
                .text
            )
        except AttributeError:
            duration_string = ""

        try:
            enrolled = soup_course.select_one(
                "#rendered-content > div > main > section:nth-of-type(2) > div > div > div:first-of-type "
                "> div:first-of-type > div > div > div:nth-of-type(2) > div:nth-of-type(4) > p > span > strong > span"
            ).text
            enrolled = int(enrolled.replace(",", ""))
        except AttributeError:
            enrolled = 0

        instructor_name = soup_course.select_one(
            "#rendered-content > div > main > section:nth-of-type(2) > div > div > div:first-of-type "
            "> div:first-of-type > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div "
            "> div:nth-of-type(2) > div:first-of-type > p > span > a",
        )
        if instructor_name:
            instructor_name = instructor_name.text.strip()
        else:
            instructor_name = ""

        try:
            summary = (
                soup_course.find("div", class_="css-12wvpfc")
                .find("p", class_="css-4s48ix")
                .text
            )
        except AttributeError:
            summary = ""

        try:
            language = soup_course.select_one(
                "#about > div > div:nth-of-type(3) > div:nth-of-type(2) > div:nth-of-type(2) > div:first-of-type > span"
            ).text
            language = language.replace("Taught in ", "")
        except AttributeError:
            language = ""

        try:
            price = soup_course.select_one(
                '[data-test="enroll-button-label"]'
            ).text.strip()
        except AttributeError:
            price = ""

        try:
            description = ""
            description_list = soup_course.find_all(
                "li", class_="cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64"
            )
            description = "\n".join([item.text for item in description_list])

        except AttributeError as e:
            description = None

        course = Course(
            name=course_name,
            tags=tags,
            difficulty=difficulty,
            instructor_name=instructor_name,
            url=url_course,
            summary=summary,
            description=description,
            reviews=reviews,
            duration=duration_string,
            enrolled=enrolled,
            rating=rating,
            language=language,
            price=price,
            image_url=image_url,
        )
        return course

    @staticmethod
    def generate_scraped_courses():
        erroneus = 0

        for i in range(1, 3):
            url = (
                COURSERA_URL
                + "/courses?page="
                + str(i)
                + "&index=prod_all_products_term_optimization"
            )
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")

            li_elements = soup.find_all("li", class_="cds-9")

            for li in li_elements:
                try:
                    yield BeatifulSoupScraper._scrape_course_details(li)
                except Exception as e:
                    print(f"Exception type: {type(e).__name__}, Message: {str(e)}")
                    print("Exception in scrapping")
                    erroneus += 1
                    continue
