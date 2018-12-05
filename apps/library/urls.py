from django.urls import path, include

from .views import MemberListView, MemberView, AvailableBookListView, OrderBorrowView, OrderReturnView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('member/', MemberListView.as_view(), name='member'), 
    path('member/<pk>/', MemberView.as_view(), name='member_detail'), 
    path('book/', AvailableBookListView.as_view(), name='book'), 
    path('borrow/', OrderBorrowView.as_view(), name='borrow'), 
    path('return/', OrderReturnView.as_view(), name='return'), 
]
