from django.contrib import admin

# Register your models here.

from catalog.models import Author, Genre, Book, BookInstance

# admin.site.register(Book)
# admin.site.register(Author) # Original, generic model admin class (defines how the admin page looks for Authors)
admin.site.register(Genre)
# admin.site.register(BookInstance)



# Define the non-generic admin classes
class AuthorAdmin(admin.ModelAdmin):
    # Sets the fields that are displayed in the admin page
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Sets the order and orientation of the admin add/detail menu for author...dates below will be horizontally-oriented.
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)




# Register the Admin classes for Book using the decorator, which wraps the class below in a function to register it.

# Add a horizontal display of the books in the library collection (foreign key)
# Be sure to add the inlines list in the class BookAdmin (a few lines below here)
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # Add a filtering option on the admin page, based off of the states of the fields listed here.
    list_filter = ('status', 'due_back')

    # Set up sections on the add/detail page:
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

