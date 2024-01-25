from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    pasth('signup', views.signup, name='signup'),
]

