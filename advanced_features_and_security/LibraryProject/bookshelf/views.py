from django.shortcuts import render

from django.contrib.auth.decorators import permission_required, login_required
from .models import Book

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
