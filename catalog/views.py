from django.shortcuts import render

# Create your views here.

# First, import the classes from the models we set up (similar to Flask importing the model functions)
from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a') -- how to do this? Mozilla django tutorial 3
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Place the data we want to put in HTML placeholders into a container and pass it on with the render function.
    # Also; include the number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



# Import the django generic view classses and inherit from them. This will render a basic list site that 
# returns the results of the query of everything in the selected model. ithin the template you can access the list 
# of books with the template variable named object_list OR book_list (i.e. generically "the_model_name_list").
# Of course, you can overwrite some of the methods in the class inherited by writing your own (for example, you might
# want to do this to pass on a subset of the data, instead of all of it).

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
# Add pagination. This also needs to be added in the html if forward and back buttons are desired.

class AuthorDetailView(generic.DetailView):
    model = Author
