import time
import asyncio
import schedule
from . import views
from django.urls import path
from .src.Parser import Parser
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('update/', views.UpdateView.as_view(), name='update'),
    path('login/', LoginView.as_view(), name='login'),
]


# def execute_parser() -> None:
#     schedule.every(6).hours.do(Parser)
#     while True:
#         schedule.run_pending()
#         time.sleep(21600)  # 6 hours
#
#
# asyncio.get_event_loop().run_in_executor(None, execute_parser)
#