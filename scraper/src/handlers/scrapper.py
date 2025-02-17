from adapters.orm import Course

class SaveCourseraCoursesHandler:
    @staticmethod
    def handle(repository, scraper):
        for course in scraper.generate_scraped_courses():
            repository.add(Course(**course.dict()))
        repository.commit()
