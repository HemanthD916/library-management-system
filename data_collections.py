import json
from book_collections import BookCollections
from patron_collections import PatronCollections
from loan_collections import LoanCollections

class DataCollections:
    def __init__(self):
        self.books = BookCollections()
        self.patrons = PatronCollections()
        self.loans = LoanCollections()

    def save_data(self):
        data = {
            'books': self.books.get_all_books(),
            'patrons': self.patrons.get_all_patrons(),
            'loans': self.loans.get_all_loans()
        }
        with open('library_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        try:
            with open('library_data.json', 'r') as f:
                data = json.load(f)
                self.books.load_books(data['books'])
                self.patrons.load_patrons(data['patrons'])
                self.loans.load_loans(data['loans'])
        except FileNotFoundError:
            pass