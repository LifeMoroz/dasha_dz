import datetime

from django.forms import Form, CharField, URLField, Textarea
from django.http import HttpResponse
from django.urls import reverse

from dasha.active_models import Person, News, TeachingMaterial, Question
from dasha import models
from dasha.forms import NewsForm, QuestionForm, TeachingMaterialForm


class ServiceLayer:
    """
    Базовый класс слоя служб.
    Пока пуст.
    """
    @classmethod
    def parse_date(cls, params):
        if 'start_date' in params:
            start_date = datetime.datetime.strptime(params.pop('start_date')[0], "%Y-%m-%d").timestamp() * 1000
            end_date = datetime.datetime.strptime(params.pop('end_date')[0], "%Y-%m-%d").timestamp() * 1000
            params['date'] = (start_date, end_date)


class NewsLayer(ServiceLayer):

    @staticmethod
    def get_edit_form():
        class EditForm(Form):
            title = CharField(label='Название', max_length=255)
            text = CharField(label='Текст новости', max_length=255, widget=Textarea)
        return EditForm

    @classmethod
    def add_news(cls, data=None):
        data = data or {}
        form = NewsForm(data)
        if form.is_valid():
            news = form.save(True)

    @classmethod
    def get_edit_context(cls, id, form=None):
        obj = News.find(id=id)[0]
        context = {'delete_url': reverse('delete_news', args=(obj.id,))}
        if form is None:
            context.update({'form': cls.get_edit_form()(initial={'title': obj.title, 'text': obj.text})})
        else:
            context.update({'form': form})
        return context

    @classmethod
    def update_news(cls, id, data):
        form = cls.get_edit_form()(data=data)
        if form.is_valid():
            obj = News.find(id=id)[0]
            obj.title = form.cleaned_data['title']
            obj.text = form.cleaned_data['text']
            obj.save()
            return True, obj
        else:
            return False, form

    @classmethod
    def get_index_context(cls, params=None):
        params = dict(params or {})
        cls.parse_date(params)
        return {"news_list": News.find(**params), "form": NewsForm()}

    @classmethod
    def delete(cls, id):
        News.find(id=id)[0].delete()


class TeachingMaterialLayer(ServiceLayer):

    @staticmethod
    def get_edit_form():
        class EditForm(Form):
            title = CharField(label='Название', max_length=255)
            dlink = URLField(label='Ссылка для скачивания', max_length=255)
        return EditForm

    @classmethod
    def add_tm(cls, data):
        data = data or {}
        form = TeachingMaterialForm(data)
        if form.is_valid():
            form.save(True)

    @classmethod
    def get_edit_context(cls, id, form=None):
        obj = TeachingMaterial.find(id=id)[0]
        context = {'delete_url': reverse('delete_tm', args=(obj.id,))}
        if form is None:
            context.update({'form': cls.get_edit_form()(initial={'title': obj.title, 'dlink': obj.dlink})})
        else:
            context.update({'form': form})
        return context

    @classmethod
    def update_tm(cls, id, data):
        form = cls.get_edit_form()(data=data)
        if form.is_valid():
            obj = TeachingMaterial.find(id=id)[0]
            obj.title = form.cleaned_data['title']
            obj.dlink = form.cleaned_data['dlink']
            obj.save()
            return True, obj
        else:
            return False, form

    @classmethod
    def get_index_context(cls, params=None):
        params = dict(params or {})
        cls.parse_date(params)
        return {"tm_list": TeachingMaterial.find(**params), "form": TeachingMaterialForm()}

    @classmethod
    def delete(cls, id):
        TeachingMaterial.find(id=id)[0].delete()


class QALayer(ServiceLayer):
    @classmethod
    def get_edit_context(cls, id, form=None):
        obj = Question.find(id=id)[0]
        if form is None:
            return {'form': cls.get_edit_form()(initial={'title': obj.title, 'text': obj.text, 'answer': obj.answer})}
        return {'form': form}

    @classmethod
    def get_edit_form(cls):
        class EditForm(Form):
            answer = CharField(label='Ответ', max_length=255, widget=Textarea)
        return EditForm

    @classmethod
    def add_answer(cls, id, POST):
        form = cls.get_edit_form()(data=POST)
        if not form.is_valid():
            return False, form

        obj = Question.find(id=id)[0]
        obj.answer = form.cleaned_data['answer']
        obj.save()
        return True, obj

    @classmethod
    def get_index_context(cls, params=None):
        params = dict(params or {})
        cls.parse_date(params)
        return {"qa_list": Question.find(**params), "form": QuestionForm()}


class PersonLayer(ServiceLayer):

    @staticmethod
    def get_auth_form():
        class AuthForm(Form):
            login = CharField(max_length=25)
            password = CharField(max_length=25)
        return AuthForm

    @staticmethod
    def authorize(login, password):
        found = Person.find(login=login, password=password)
        if found:
            return found[0]
        return None

    @staticmethod
    def is_auth(COOKIES):
        found = Person.find(id=COOKIES.get('user_id'))
        if found:
            return True
        else:
            return False

    @staticmethod
    def get_auth_context(form=None):
        if form is None:
            return {'form': PersonLayer.get_auth_form()}
        else:
            return {'form': form}

    @staticmethod
    def get_index_context(COOKIES):
        found = Person.find(id=COOKIES.get('user_id'))
        return {
            'person': found[0]
        }

    @staticmethod
    def set_auth(response: HttpResponse, form_data):
        form = PersonLayer.get_auth_form()(data=form_data)
        if form.is_valid():
            response.set_cookie('user_id', Person.find(login=form.cleaned_data['login'], password=form.cleaned_data['password'])[0].id)
            return True, response
        else:
            return False, form