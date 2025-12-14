class Loan:
    def __init__(self, loan_id, book_id, patron_id, due_date, status="normal"):
        self.loan_id = loan_id
        self.book_id = book_id
        self.patron_id = patron_id
        self.due_date = due_date
        self.status = status

    def __str__(self):
        return f"Loan({self.loan_id}, {self.book_id}, {self.patron_id}, {self.due_date}, {self.status})"