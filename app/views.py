from django.db.models import Q, QuerySet
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse, JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from app.src.Parser import Parser
from app.models import Phones


class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'app/index.html'

    def get(self, request, *args) -> HttpResponse:
        return render(request, self.template_name)


class SearchView(FormView):
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args) -> JsonResponse | HttpResponse:
        name: str = request.POST['search']

        phones: QuerySet = Phones.objects.filter(name_lower__search=name.lower())\
            .order_by('name')\
            .values('shop', 'name', 'current_price', 'before_discount')

        return JsonResponse(list(phones), safe=False)


class UpdateView(FormView):  # new parsing for all sites
    http_method_names = ['post']

    def post(self, request: WSGIRequest, *args) -> HttpResponse:
        Parser()

        return HttpResponse(None)
