class Book:
    def __init__(self, author, title, isbn, book_id, cost, status="In"):
        self.author = author
        self.title = title
        self.isbn = isbn
        self.book_id = book_id
        self.cost = cost
        self.status = status

    def __str__(self):
        return f"Book({self.title}, {self.author}, {self.isbn}, {self.book_id}, {self.cost}, {self.status})"