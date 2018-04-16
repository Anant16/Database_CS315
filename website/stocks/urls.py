# from django.conf.urls import url
# from stocks import views

# urlpatterns = [
#     url(r'^$', views.index, name='stocks_index'),
# ]

from django.conf.urls import include, url
from stocks.views import *


urlpatterns = [
    url(r'^$', portfolio, name='portfolio'),
    url(r'^historical/?$', historical, name='historical'),
    url(r'^query/?$', query, name='query'),
    url(r'^symbolInfo/?$', symbolInfo, name='symbolInfo'),
    url(r'^dayInfo/?$', dayInfo, name='dayInfo'),
    url(r'^lastUpdated/?$', lastUpdated, name='lastUpdated'),
    url(r'^UpdateDatabase/?$', UpdateDatabase, name='UpdateDatabase'),
]