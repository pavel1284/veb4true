from django.urls import path
from django.contrib import admin
from .views import (
    register_view, login_view, logout_view, book_list, add_book,
    edit_book, book_delete, book_detail, profile_view, add_to_cart,
    cart_view, create_order, order_history
)

urlpatterns = [
    path('', book_list, name='home'),
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('books/', book_list, name='book_list'),
    path('books/add/', add_book, name='add_book'),
    path('books/edit/<int:pk>/', edit_book, name='edit_book'),
    path('books/delete/<int:pk>/', book_delete, name='delete_book'),
    path('books/<int:pk>/', book_detail, name='book_detail'),
    path('profile/', profile_view, name='profile'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('order/create/', create_order, name='create_order'),
    path('orders/', order_history, name='order_history'),
]