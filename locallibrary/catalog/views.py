import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book(request, bookinstance_id):
    book_instance = get_object_or_404(BookInstance, pk=bookinstance_id)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('catalog:borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {'form': form, 'book_instance': book_instance}

    return render(request, 'catalog/book_renew.html', context=context)


class BookListView(generic.ListView):
    model = Book
    template_name = 'catalog/books.html'
    context_object_name = 'book_list'
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'


class BookCreate(PermissionRequiredMixin, generic.edit.CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    template_name = 'catalog/book_form.html'
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    template_name = 'catalog/book_form.html'
    permission_required = 'catalog.can_mark_returned'


class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/authors.html'
    context_object_name = 'author_list'
    paginate_by = 3


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'


class AuthorCreate(PermissionRequiredMixin, generic.edit.CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_form.html'
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Author
    template_name = 'catalog/author_delete_form.html'
    success_url = reverse_lazy('catalog:authors')
    permission_required = 'catalog.can_mark_returned'


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/list_borrowed.html'
    paginate_by = 10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
