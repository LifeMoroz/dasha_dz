from datetime import datetime

from db.active_record import BaseActiveRecord, Field


class Person(BaseActiveRecord):
    table_name = 'person'
    first_name = Field()
    last_name = Field()
    login = Field()
    password = Field()
    phone = Field()


class News(BaseActiveRecord):
    table_name = 'news'
    title = Field()
    text = Field()
    date = Field()

    def clean_date(self, date):
        if date:
            date = datetime.fromtimestamp(int(date) / 1000.)
        return date


class TeachingMaterial(BaseActiveRecord):
    table_name = 'teaching_material'
    title = Field()
    dlink = Field()
    description = Field()
    date = Field()

    def clean_date(self, date):
        if date:
            date = datetime.fromtimestamp(int(date) / 1000.)
        return date


class Question(BaseActiveRecord):
    table_name = 'question'
    title = Field()
    text = Field()
    answer = Field()
    to_teacher = Field()
    date = Field()

    def clean_date(self, date):
        if date:
            date = datetime.fromtimestamp(int(date) / 1000.)
        return date
