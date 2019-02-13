from django.urls import path
from django.conf.urls import include
from . import views


# Arguments of path function: a URL pattern, a view function that will be called if the URL pattern is 
# detected (this one comes from the function index() in the views.py file), and a name that we can use in 
# href statements.

# Additionally, the use of <something> in the url pattern will capture the input url in that place and save
# it to the variable 'something'. In this case, the int:pk will capture an integer named 'pk' (as a book id).

# you can use more complex pattern matching with regex, by using the re_path() method instead of the path() one
# There is more info about this at https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Generic_views.
urlpatterns = [
    path('', views.index, name='index'),    # New line as per tutorial
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
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


# Registration/authentication/permission tutorial pages:
urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedBooksAll.as_view(), name='all-borrowed'),
]

# Form tutorial pages (note that the <uuid:pk> will look for a properly-formatted uuid and pass it into the view as pk):
urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
