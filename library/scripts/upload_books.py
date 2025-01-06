import pandas as pd
from library.models import Book, Author
from datetime import timedelta

def run():
    # Read CSV file into a DataFrame
    csv_file_path = 'books.csv'
    df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")

    # Iterate through the DataFrame and create model instances
    for index, row in df.iterrows():
        author_data = str(row['authors']).lower().split(" and ")
        authors = []
        for author in author_data:
            author, _ = Author.objects.get_or_create(
                name=author,
            )
            authors.append(author)

        # Create the Book instance
        book = Book(
            title=row['title'],
            rent_cost=row['cost'],
            max_rent_period=timedelta(days=30),
        )
        # to save the current product
        book.save()
        print(authors)
        book.author.add(*list(map(lambda a: a.id, authors)))

    print("CSV data has been loaded into the Django database.")
