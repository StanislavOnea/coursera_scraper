from orm import Course
from sqlalchemy.future import select
import abc

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, course: Course):
        raise NotImplementedError


class SqlAlchemyAsyncRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        
    def add(self, course: Course):
        self.session.add(course)

    async def commit(self):
        await self.session.commit()

    async def list(self):
        result = await self.session.execute(select(Course))
        return result.scalars().all()
