from datetime import datetime

from django.db import models


class Person(models.Model):
    table_name = 'person'
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    class Meta:
        db_table = 'person'


class TimestampModel(models.Model):
    date = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date = datetime.now().timestamp()
        super(TimestampModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class News(TimestampModel, models.Model):
    table_name = 'news'
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

    class Meta:
        db_table = 'news'


class TeachingMaterial(TimestampModel, models.Model):
    table_name = 'teaching_material'
    title = models.CharField(max_length=255)
    dlink = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = 'teaching_material'


class Question(TimestampModel, models.Model):
    table_name = 'question'
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=1024)
    answer = models.CharField(max_length=255)
    to_teacher = models.IntegerField()

    class Meta:
        db_table = 'question'
