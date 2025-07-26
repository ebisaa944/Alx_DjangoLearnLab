from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from .models import Book

from django.shortcuts import get_object_or_404
from django.db.models import Q

from .forms import ExampleForm

def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data
            return render(request, 'bookshelf/form_success.html')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

def safe_search(request):
    search_term = request.GET.get('q', '')
    
    # Safe ORM query - prevents SQL injection
    results = Book.objects.filter(
        Q(title__icontains=search_term) |
        Q(author__icontains=search_term)
    )
    
    # Never do this (vulnerable to SQL injection):
    # query = "SELECT * FROM bookshelf_book WHERE title LIKE '%" + search_term + "%'"
    # results = Book.objects.raw(query)
    
    return render(request, 'bookshelf/search_results.html', {'results': results})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'bookshelf/book_form.html')

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_update(request, pk):
    book = Book.objects.get(pk=pk)
    # Handle form submission
    return render(request, 'bookshelf/book_form.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = Book.objects.get(pk=pk)
    # Handle deletion
    return redirect('book_list')
