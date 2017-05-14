"""
Базовая функциональность классов ActiveRecord
"""
import datetime

from db.db import Database


class Field:
    """
    Класс носит информативную функцию
    Его инстансом инициализруются все поля классов, которые ожидается увидеть в БД
    """
    pass


class BaseActiveRecord:
    """
    Базовый класс ActiveRecord
    Поскольку он может нести часть бизнес логики, то уникальные ключи записей формируются прямо внутри него
    Следует паттерну Lazy загрузки.
    Если какие-то поля не инициалированны в конструкторе, то могут быть инициализрованы позднее.
    Окончательная проверка выполняется в методе `save` который записывает данные в базу

    Так же включает в себя логику формирования поискового запроса в базу
    """
    table_name = None
    id = Field()  # PK by default

    def __init__(self, *args, **kwargs):
        # Умная сборка объекта. Все что передано проставляем в объект.
        # Наследники будут определять что должно быть.
        if args:
            for i, key in enumerate(self.fields()):
                value = args[i]
                if hasattr(self, 'clean_' + key):
                    value = getattr(self, 'clean_' + key)(value)
                setattr(self, key, value)
        else:
            raise Exception

    @classmethod
    def fields(cls):
        fields = []
        for key in dir(cls):
            if isinstance(getattr(cls, key), Field):
                fields.append(key)
        return fields

    @classmethod
    def find(cls, date=None, **kwargs):
        where = ''
        data = []
        for key, value in kwargs.items():
            where += ' and '
            if isinstance(value, list):
                where += '{} IN ({})'.format(key, ', '.join([str(x) for x in value]))
            else:
                where += '{}=?'.format(key)
                data.append(value)
        if date:
            where += ' and {} < date and date < {}'.format(date[0], date[1])
        sql = "SELECT {fields} FROM {table_name} where 1{where}".format(fields=', '.join(cls.fields()), table_name=cls.table_name, where=where)
        result = []
        for row in Database.get_database().execute(sql, data).fetchall():
            result.append(cls(*row))
        return result

    def save(self):
        to_save = {}
        for key in self.fields():
            if key == 'date':
                to_save[key] = getattr(self, key).timestamp() * 1000
                continue
            to_save[key] = getattr(self, key)
            if key == 'id' and not isinstance(to_save[key], int):  # Получаем новый id
                to_save['id'] = max([x.id for x in self.find()] or [0]) + 1
                setattr(self, 'id', to_save['id'])
        fields = ', '.join(to_save.keys())
        values = ':' + ', :'.join(to_save.keys())
        sql = "REPLACE INTO {table_name} ({fields}) VALUES ({values})"
        sql = sql.format(table_name=self.table_name, fields=fields, values=values)
        Database.get_database().execute(sql, to_save)
        return self

    def delete(self):
        sql = "DELETE FROM {table_name} WHERE id={id}".format(table_name=self.table_name, id=self.id)
        Database.get_database().execute(sql)
