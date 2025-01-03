from .models import Book
from json import JSONEncoder


class BookEncoder(JSONEncoder):
    def default(self, o):
        if not isinstance(o, Book):
            return super().default(o)
        d = {
            "id": o.id,
            "title": o.title,
            "authors": ",".join(o.author.values_list("name", flat=True)),
            # "rent_cost": o.rent_cost,
            # "max_rent_period": o.max_rent_period,
        }
        return d
