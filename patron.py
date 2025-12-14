class Patron:
    def __init__(self, name, id_number, fine_balance=0.0, current_books_out=0):
        self.name = name
        self.id_number = id_number
        self.fine_balance = fine_balance
        self.current_books_out = current_books_out

    def __str__(self):
        return f"Patron({self.name}, {self.id_number}, {self.fine_balance}, {self.current_books_out})"