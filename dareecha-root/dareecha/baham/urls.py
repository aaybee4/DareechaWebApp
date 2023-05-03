from . import views
from django.urls import path, include

urlpatterns=[
    path('', views.view_home, name='home'),
    path('p1', views.view_p1, name='page1')
]