from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response

from .models import Member, Book, OrderBorrow, OrderReturn
from .serializers import MemberSerializer, BookSerializer, OrderBorrowSerializer, OrderReturnSerializer


class MemberListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class MemberView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class AvailableBookListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Book.objects.filter(is_borrowed=False)
    serializer_class = BookSerializer


class OrderBorrowView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = OrderBorrow.objects.all()
    serializer_class = OrderBorrowSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = OrderBorrowSerializer(data=request.data)
            if serializer.is_valid(raise_exception=ValueError):
                borrow = serializer.save()
                if borrow:
                    serializer_data = serializer.data
                    serializer_data.update(is_returned=borrow.is_returned(), return_schedule=borrow.get_return_schedule())
                    return Response(serializer_data, status=status.HTTP_201_CREATED)
            return Response(serializer.error_messages,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response("Book out of stock",
                            status=status.HTTP_400_BAD_REQUEST)


class OrderReturnView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = OrderReturn.objects.all()
    serializer_class = OrderReturnSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderReturnSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            order_return = serializer.save()
            if order_return:
                serializer_data = serializer.data
                serializer_data.update(charge=order_return.get_charge())
                return Response(serializer_data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
