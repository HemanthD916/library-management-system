import datetime
from loan import Loan

class LoanCollections:
    def __init__(self):
        self.loans = {}

    def add_loan(self, loan):
        self.loans[loan.loan_id] = loan

    def edit_loan(self, loan_id, **kwargs):
        if loan_id in self.loans:
            for key, value in kwargs.items():
                if value.strip():
                    if key == 'due_date':
                        try:
                            value = datetime.datetime.fromisoformat(value)
                        except ValueError:
                            print("Invalid due date format (use YYYY-MM-DDTHH:MM:SS); skipping.")
                            continue
                    setattr(self.loans[loan_id], key, value)

    def delete_loan(self, loan_id):
        if loan_id in self.loans:
            del self.loans[loan_id]

    def find_loan(self, loan_id):
        return self.loans.get(loan_id)

    def list_loans(self):
        for loan in self.loans.values():
            print(loan)

    def list_overdue_loans(self):
        overdue_loans = [loan for loan in self.loans.values() if loan.status == "overdue"]
        for loan in overdue_loans:
            print(loan)

    def list_books_for_patron(self, patron_id):
        patron_loans = [loan for loan in self.loans.values() if loan.patron_id == patron_id]
        for loan in patron_loans:
            print(loan)

    def update_loan_status(self, patrons):
        current_time = datetime.datetime.now()
        for loan in self.loans.values():
            if isinstance(loan.due_date, str):
                loan.due_date = datetime.datetime.fromisoformat(loan.due_date)
            if loan.due_date < current_time and loan.status != "overdue":
                loan.status = "overdue"
                patron = patrons.find_patron(loan.patron_id)
                if patron:
                    patron.fine_balance += (current_time - loan.due_date).days * 0.25

    def pay_fines(self, patron_id, amount, patrons):
        patron = patrons.find_patron(patron_id)
        if patron:
            patron.fine_balance -= amount

    def report_lost(self, loan_id, patrons, books):
        loan = self.loans.get(loan_id)
        if loan:
            patron = patrons.find_patron(loan.patron_id)
            book = books.find_book(loan.book_id)
            if patron and book:
                patron.fine_balance += book.cost
                book.status = "Lost"
                self.delete_loan(loan_id)

    def get_all_loans(self):
        return {k: self._loan_to_dict(v) for k, v in self.loans.items()}

    def _loan_to_dict(self, loan):
        d = vars(loan)
        if isinstance(d['due_date'], datetime.datetime):
            d['due_date'] = d['due_date'].isoformat()
        return d

    def load_loans(self, loans):
        self.loans = {int(k): Loan(**self._prepare_loan_dict(v)) for k, v in loans.items()}

    def _prepare_loan_dict(self, v):
        if 'due_date' in v and isinstance(v['due_date'], str):
            v['due_date'] = datetime.datetime.fromisoformat(v['due_date'])
        return v

    def manage_loans(self, patrons, books, save_data):
        while True:
            choice = input("Manage Loans\n1. Add\n2. Edit\n3. Delete\n4. Find\n5. List\n6. Overdue\n7. Patron's Books\n8. Update Status\n9. Pay Fines\n10. Report Lost\n11. Back\nPlease enter a number from above: ")
            if choice == '1':
                try:
                    loan_id = int(input("Loan ID (numbers only): "))
                    book_id = int(input("Book ID (numbers only): "))
                    patron_id = int(input("Patron ID (numbers only): "))
                    self.add_loan(Loan(loan_id, book_id, patron_id, datetime.datetime.now() + datetime.timedelta(days=10)))
                except ValueError:
                    print("Invalid input; try again.")
            elif choice == '2':
                loan_id = int(input("Loan ID (numbers only): "))
                print("Leave blank to keep current value.")
                new_due = input("New due date (YYYY-MM-DDTHH:MM:SS): ")
                new_status = input("New status: ")
                self.edit_loan(loan_id, due_date=new_due, status=new_status)
            elif choice == '3':
                self.delete_loan(int(input("Loan ID (numbers only): ")))
            elif choice == '4':
                print(self.find_loan(int(input("Loan ID (numbers only): "))))
            elif choice == '5':
                self.list_loans()
            elif choice == '6':
                self.list_overdue_loans()
            elif choice == '7':
                self.list_books_for_patron(int(input("Patron ID (numbers only): ")))
            elif choice == '8':
                self.update_loan_status(patrons)
            elif choice == '9':
                try:
                    self.pay_fines(int(input("Patron ID (numbers only): ")), float(input("Amount: $")), patrons)
                except ValueError:
                    print("Invalid input; try again.")
            elif choice == '10':
                self.report_lost(int(input("Loan ID (numbers only): ")), patrons, books)
            elif choice == '11':
                save_data()
                break