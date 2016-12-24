from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from dasha.service_layer import PersonLayer, NewsLayer, TeachingMaterialLayer, QALayer


class IndexView(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            context = PersonLayer.get_index_context(request.COOKIES)
            context.update(NewsLayer.get_index_context())
            context.update(TeachingMaterialLayer.get_index_context())
            context.update(QALayer.get_index_context())
            return render(request, 'index.html', context)
        return render(request, 'auth.html', PersonLayer.get_auth_context())


class AuthView(View):
    def post(self, request):
        response = HttpResponseRedirect(reverse('index'))
        success, response = PersonLayer.set_auth(response, request.POST)
        if success:
            return response
        else:
            return render(request, 'auth.html', PersonLayer.get_auth_context())


class NewsAdd(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            news = NewsLayer.add_news()
            return HttpResponseRedirect(reverse('edit_news', args=(news.id,)))
        else:
            return HttpResponseRedirect(reverse('index'))


class TMAdd(View):
    def get(self, request):
        if PersonLayer.is_auth(request.COOKIES):
            tm = TeachingMaterialLayer.add_tm()
            return HttpResponseRedirect(reverse('edit', args=(tm.id,)))
        else:
            return HttpResponseRedirect(reverse('index'))


class TMEdit(View):
    def get(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', TeachingMaterialLayer.get_edit_context(id))

    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        success, form = TeachingMaterialLayer.update_tm(id, request.POST)
        if success:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', TeachingMaterialLayer.get_edit_context(id, form))


class NewsEdit(View):
    def get(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', NewsLayer.get_edit_context(id))

    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        success, form = NewsLayer.update_news(id, request.POST)
        if success:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', NewsLayer.get_edit_context(id, form))


class AddAnswer(View):
    def get(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', QALayer.get_edit_context(id))

    def post(self, request, id):
        if not PersonLayer.is_auth(request.COOKIES):
            return HttpResponseRedirect(reverse('index'))
        success, form = QALayer.add_answer(id, request.POST)
        if success:
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'edit.html', QALayer.get_edit_context(id, form))


class NewsDelete(View):
    def get(self, request, id):
        if PersonLayer.is_auth(request.COOKIES):
            NewsLayer.delete(id=id)
        return HttpResponseRedirect(reverse('index'))


class TMDelete(View):
    def get(self, request, id):
        if PersonLayer.is_auth(request.COOKIES):
            TeachingMaterialLayer.delete(id=id)
        return HttpResponseRedirect(reverse('index'))
