from django.db.models import Q, QuerySet
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from app.src.Parser import Parser
from app.models import Phones


class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'app/index.html'

    def get(self, request: WSGIRequest, *args) -> render or redirect:
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, self.template_name)


class SearchView(FormView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args) -> JsonResponse or HttpResponse or redirect:
        if not request.user.is_authenticated:
            return redirect('login')

        name: str = request.POST['search']

        phones: QuerySet = Phones.objects.filter(name_lower__search=name.lower())\
            .order_by('name')\
            .values('shop', 'name', 'current_price', 'before_discount')

        return JsonResponse(list(phones), safe=False)


class UpdateView(FormView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args) -> HttpResponse or redirect:
        if not request.user.is_superuser:
            return redirect('/')

        Parser()
        return HttpResponse(None)

