from book import Book

class BookCollections:
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        if not str(book.book_id).isdigit():
            raise ValueError("Book ID must be numbers only.")
        self.books[book.book_id] = book

    def edit_book(self, book_id, **kwargs):
        if book_id in self.books:
            for key, value in kwargs.items():
                if value.strip():  # Skip if blank
                    if key == 'cost':
                        try:
                            value = float(value)
                        except ValueError:
                            print("Invalid cost; skipping.")
                            continue
                    elif key == 'book_id':
                        try:
                            value = int(value)
                        except ValueError:
                            print("Invalid book ID; skipping.")
                            continue
                    setattr(self.books[book_id], key, value)

    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]

    def find_book(self, book_id):
        return self.books.get(book_id)

    def list_books(self):
        for book in self.books.values():
            print(book)

    def get_all_books(self):
        return {k: vars(v) for k, v in self.books.items()}

    def load_books(self, books):
        self.books = {int(k): Book(**v) for k, v in books.items()}

    def manage_books(self):
        while True:
            choice = input("Manage Books\n1. Add\n2. Edit\n3. Delete\n4. Find\n5. List\n6. Back\nEnter choice: ")
            if choice == '1':
                try:
                    book_id = int(input("Book ID (numbers only): "))
                    cost = float(input("Cost: $"))
                    self.add_book(Book(input("Author: "), input("Title: "), input("ISBN (numbers and letters only): "), book_id, cost))
                except ValueError:
                    print("Invalid input; try again.")
            elif choice == '2':
                book_id = int(input("Book ID (numbers only): "))
                print("Leave blank to keep current value.")
                self.edit_book(book_id, author=input("New author: "), title=input("New title: "), 
                               isbn=input("New ISBN (numbers and letters only): "), cost=input("New cost: $"), status=input("New status: "))
            elif choice == '3':
                self.delete_book(int(input("Book ID (numbers only): ")))
            elif choice == '4':
                print(self.find_book(int(input("Book ID (numbers only): "))))
            elif choice == '5':
                self.list_books()
            elif choice == '6':
                break