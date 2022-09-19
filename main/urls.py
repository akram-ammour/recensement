from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('<int:id>',views.pdf, name="pdf"),
    path('test',views.test, name="test"),
]
