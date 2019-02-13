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
# returns the results of the query of everything in the selected model. Within the template you can access the list 
# of books with the template variable named object_list OR book_list (i.e. generically "the_model_name_list").
# Of course, you can overwrite some of the methods in the class inherited by writing your own (for example, you might
# want to do this to pass on a subset of the data, instead of all of it). 

# Doesn't appear that you need to call the return statement for the class-based views. How do they know which template to
# use? Good question. Maybe there is a generic convention? 

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

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAll(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    # Set the template to grab.
    template_name ='catalog/bookinstance_all_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# Below is the views for the forms.

import datetime
from django.contrib.auth.decorators import permission_required

# Return an object specified by its primary key from a model or raise Http404 exception.
from django.shortcuts import render, get_object_or_404

# Creates a redirect to a specified URL
from django.http import HttpResponseRedirect

# Generates a URL from URL config name...python equiv to the url tag used in the template files.
from django.urls import reverse

# Import the form we created from forms.py
from catalog.forms import RenewBookForm

# This view function requires permission. Then, it checks for a POST or GET request. Since we want our actual
# request to be POST, we can use this method. Use other methods if the actual request will be GET. In this case,
# the first time a website is called is a GET, so it sets up the instance of our form class with default values.
# If being submitted, then the request is POST and the answers are "bound" to the form instance (so that we have
# a record of what errors occured in the submissions), and then validated. If not valid, return to form page but
# use the saved errors-including instance to create the page. 

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
