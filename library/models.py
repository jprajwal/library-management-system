from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    name = models.TextField()


class Book(models.Model):
    title = models.TextField()
    author = models.ManyToManyField(Author, related_name="books")
    rent_cost = models.IntegerField()
    max_rent_period = models.DurationField()

    def __str__(self) -> str:
        return str(self.title)

    def get_author_ids(self) -> list[int]:
        return [i for ids in self.author.values_list("id") for i in ids]

    def get_max_rent_period_as_int(self) -> int:
        return int(self.max_rent_period.days)


class BookCopy(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    def get_book_id(self) -> int:
        return self.book_id.id


class PaymentStatus(models.TextChoices):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"


class Payment(models.Model):
    payment_datetime = models.DateTimeField()
    payment_status = models.CharField(
        choices=PaymentStatus,
        default=PaymentStatus.PENDING,
        max_length=10,
    )


class TransactionStatus(models.TextChoices):
    PENDING = "pending"
    SUCCESS = "success"
    FAILURE = "failure"


class Transaction(models.Model):
    member_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_status = models.CharField(
        choices=TransactionStatus,
        default=TransactionStatus.PENDING,
        max_length=10,
    )
    transaction_datetime = models.DateTimeField()
    payment_id = models.ForeignKey(
        Payment, on_delete=models.RESTRICT, null=True)


class BookRentStatus(models.TextChoices):
    BORROWED = "borrowed"
    RETURNED = "returned"


class BookRent(models.Model):
    bookcopy_id = models.OneToOneField(
        BookCopy, on_delete=models.CASCADE, unique=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    cost = models.IntegerField(null=True)
    transaction_id = models.ForeignKey(
        Transaction,
        on_delete=models.RESTRICT,
        null=True,
        related_name='rented_books',
    )
    return_transaction_id = models.ForeignKey(
        Transaction,
        on_delete=models.RESTRICT,
        null=True,
        related_name='returned_books',
    )
    status = models.CharField(
        choices=BookRentStatus,
        default=BookRentStatus.BORROWED,
        max_length=10,
    )


class CartItemType(models.TextChoices):
    BOOK = "book"


class CartItem(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type = models.CharField(
        choices=CartItemType,
        default=CartItemType.BOOK,
        max_length=10,
    )
    product_id = models.IntegerField()
    requested_count = models.IntegerField()
