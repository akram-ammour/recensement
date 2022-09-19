from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("main.urls")),
    path('jsontest/', include("jsontest.urls"))
]
handle404 = "main.views.handle404"