from django.urls import path
from django.urls import re_path as url
from . import views


urlpatterns=[
    url(r'^covid/$',views.covid_data_api),
    url(r'^covid/([0-9]{4}-[0-9]{2}-[0-9]{2})$',views.covid_data_api),
    url(r'^login/', views.LoginView.as_view()),
   
]