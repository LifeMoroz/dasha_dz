from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from dasha.service_layer import PersonLayer, NewsLayer, TeachingMaterialLayer, QALayer


class NewsList(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            context = PersonLayer.get_index_context(request.COOKIES)
            context.update(NewsLayer.get_index_context(request.GET))
            return render(request, 'news.html', context)
        return render(request, 'auth.html', PersonLayer.get_auth_context())


class TMList(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            context = PersonLayer.get_index_context(request.COOKIES)
            context.update(TeachingMaterialLayer.get_index_context(request.GET))
            return render(request, 'materials.html', context)
        return render(request, 'auth.html', PersonLayer.get_auth_context())


class AnswersList(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            context = PersonLayer.get_index_context(request.COOKIES)
            context.update(QALayer.get_index_context(request.GET))
            return render(request, 'answers.html', context)
        return render(request, 'auth.html', PersonLayer.get_auth_context())


class AuthView(View):
    def post(self, request):
        response = HttpResponseRedirect(reverse('news-list'))
        success, response = PersonLayer.set_auth(response, request.POST)
        if success:
            return response
        else:
            return render(request, 'auth.html', PersonLayer.get_auth_context())


class NewsAdd(View):
    def post(self, request):
        NewsLayer.add_news(request.POST)
        return HttpResponseRedirect(reverse('news-list'))


class TMAdd(View):
    def post(self, request):
        TeachingMaterialLayer.add_tm(request.POST)
        return HttpResponseRedirect(reverse('material-list'))


class TMEdit(View):
    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('material-list'))
        TeachingMaterialLayer.update_tm(id, request.POST)
        return HttpResponseRedirect(reverse('material-list'))


class NewsEdit(View):
    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('news-list'))
        NewsLayer.update_news(id, request.POST)
        return reverse('news-list')


class AddAnswer(View):
    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('answers-list'))
        QALayer.add_answer(id, request.POST)
        return reverse('answers-list')


class NewsDelete(View):
    def get(self, request, id):
        if PersonLayer.is_auth(request.COOKIES):
            NewsLayer.delete(id=id)
        return HttpResponseRedirect(reverse('news-list'))


class TMDelete(View):
    def get(self, request, id):
        TeachingMaterialLayer.delete(id=id)
        return HttpResponseRedirect(reverse('material-list'))
