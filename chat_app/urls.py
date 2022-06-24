from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('chat/', messages_page),
]
