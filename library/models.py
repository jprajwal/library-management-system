from django.db import models
import json


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


class Member(models.Model):
    name = models.TextField()
    email_id = models.EmailField()


class BookRent(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    bookcopy_id = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    start_date = models.DateField()
    due_date = models.DateField()


class Cart(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)