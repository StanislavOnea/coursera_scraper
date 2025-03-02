from orm import Course
import time

class SaveCourseraCoursesHandler:
    @staticmethod
    async def handle(repository, scraper):
        counter = 0
        try:
            async for course in scraper.scrape_courses():
                repository.add(Course(**course.dict()))
                counter += 1
                if counter == 10:
                    await repository.commit()
            await repository.commit()
        finally:
            await scraper.http_client.session.close()
