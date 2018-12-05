from django.contrib import admin

from .models import Member, Book, OrderBorrow, OrderReturn


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'is_borrowed']
    list_editable = ['is_borrowed']


@admin.register(OrderBorrow)
class OrderBorrowAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'borrow_at']


@admin.register(OrderReturn)
class OrderReturnAdmin(admin.ModelAdmin):
    list_display = ['borrow', 'return_at']
