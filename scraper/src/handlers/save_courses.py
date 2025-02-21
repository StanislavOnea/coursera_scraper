from adapters.orm import Course

class SaveCourseraCoursesHandler:
    @staticmethod
    async def handle(repository, scraper):
        # for course in scraper.generate_scraped_courses():
        #     repository.add(Course(**course.dict()))
        # repository.commit()

        try:
            async for course in scraper.scrape_courses():
                repository.add(Course(**course.dict()))
        finally:
            await scraper.http_client.session.close()