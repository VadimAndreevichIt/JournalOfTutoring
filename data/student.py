import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    data_lesson = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_student = sqlalchemy.Column(sqlalchemy.String)

    def get_info(self):
        temp = self.data_lesson.split(";")
        day = []
        time = {}
        for i in temp:
            day.append(i.split("-")[0])
            time[i.split("-")[0]] = i.split("-")[1]
        return [str(self.id), self.name, self.link, self.phone, day, time, self.class_student]
