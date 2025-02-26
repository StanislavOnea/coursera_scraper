from adapters.orm import Course
import time

class SaveCourseraCoursesHandler:
    @staticmethod
    async def handle(repository, scraper):
        # for course in scraper.generate_scraped_courses():
        #     repository.add(Course(**course.dict()))
        # repository.commit()
        s = time.time()
        try:
            async for course in scraper.scrape_courses():
                repository.add(Course(**course.dict()))
                print(f"saved {course.name}")
        finally:
            await scraper.http_client.session.close()

        e = time.time()

        print(f"Time is {e - s}")
