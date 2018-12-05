from rest_framework import serializers

from .models import Member, Book, OrderBorrow, OrderReturn


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class OrderBorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBorrow
        fields = '__all__'


class OrderReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderReturn
        fields = '__all__'
