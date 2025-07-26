from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """Query all books by a specific author"""
    return Book.objects.filter(author__name=author_name)

def get_books_in_library(library_name):
    """List all books in a library"""
    return Library.objects.get(name=library_name).books.all()

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    return Librarian.objects.get(library__name=library_name)

# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)
