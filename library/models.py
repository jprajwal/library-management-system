from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.TextField()


class Book(models.Model):
    title = models.TextField()
    rent_cost = models.IntegerField()
    max_rent_period = models.DurationField()


class BookCopy(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)


class Member(models.Model):
    name = models.TextField()
    email_id = models.EmailField()


class BookRent(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    bookcopy_id = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()
