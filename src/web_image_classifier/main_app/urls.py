from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.main, name='main'),
    path("information/", views.information, name="information"),
    path("statistic/", views.statistic, name="statistic"),
    path("results/", views.results, name="results"),
]
