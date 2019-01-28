from django.urls import path
from . import views

# Arguments of path function: a URL pattern, a view function that will be called if the URL pattern is 
# detected (this one comes from the function index() in the views.py file), and a name that we can use in 
# href statements.
urlpatterns = [
    path('', views.index, name='index'),    # New line as per tutorial
]

# New lines below to serve static files in debug mode
import os
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': os.path.join(BASE_DIR, 'catalog/static'),
        }),
    ]
