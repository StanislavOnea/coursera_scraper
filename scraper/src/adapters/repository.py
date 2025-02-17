from model.courses import Course
import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, course: Course):
        raise NotImplementedError



class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        

    def add(self, course: Course):
        self.session.add(course)

    def commit(self):
        self.session.commit()
