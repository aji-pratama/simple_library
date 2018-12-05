import datetime

from django.core.exceptions import ValidationError
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='created at')


class Member(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name


class Book(BaseModel):
    name = models.CharField(max_length=254)
    author = models.CharField(max_length=50)
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_stock(self):
        return Book.objects.filter(name=self.name, author=self.author, is_borrowed=False).count()


class OrderBorrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrow_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.book.name

    def save(self, *args, **kwargs):
        if self.book.is_borrowed == True:
            raise ValidationError("Book out of stock")
        else:
            self.book.is_borrowed = True
            self.book.save()
        super(OrderBorrow, self).save(*args, **kwargs)

    def is_returned(self):
        returned = None
        try:
            self.orderreturn
            returned = True
        except:
            returned = False
        return returned

    def get_return_schedule(self):
        return self.borrow_at + datetime.timedelta(7)


class OrderReturn(models.Model):
    borrow = models.OneToOneField(OrderBorrow, on_delete=models.CASCADE)
    return_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.borrow.book.is_borrowed = False
        self.borrow.book.save()
        super(OrderReturn, self).save(*args, **kwargs)

    def get_charge(self):
        charge = 0
        if self.return_at > self.borrow.get_return_schedule():
            charge = (self.borrow.get_return_schedule - self.return_at) * 1000
        return charge
