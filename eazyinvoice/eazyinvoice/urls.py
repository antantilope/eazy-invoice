

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseNotFound

urlpatterns = [
    path('', include("api.urls")),
    path('admin/login/', lambda requst: HttpResponseNotFound()),
    path('admin/logout/', lambda requst: HttpResponseNotFound()),
    path('admin/', admin.site.urls),
]
