from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, CustomUser, CartItem, Order, OrderItem
from .forms import BookForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.core.paginator import Paginator
from django.contrib import messages


def book_list(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


@user_passes_test(lambda u: u.role == 'admin')
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_edit.html', {'form': form})


@user_passes_test(lambda u: u.role == 'admin')
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('book_list')


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'books/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'books/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'books/profile.html', {'form': form})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f'Added {book.title} to cart')
    return redirect('book_list')


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)
    return render(request, 'books/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, 'Your cart is empty')
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(user=request.user)
        total_price = 0
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            total_price += item.get_total_price()
        order.total_price = total_price
        order.save()
        cart_items.delete()
        messages.success(request, 'Order created successfully')
        return redirect('order_history')

    return redirect('cart')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/order_history.html', {'orders': orders})