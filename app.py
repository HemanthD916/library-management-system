from flask import Flask, render_template, request, redirect, url_for, flash
from library import Library
import json  # For any extra JSON handling if needed

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # For flash messages; change in production

library = Library()  # Initialize your Library instance

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'add':
                book_id = int(request.form['book_id'])
                cost = float(request.form['cost'])
                library.books.add_book(Book(
                    request.form['author'],
                    request.form['title'],
                    request.form['isbn'],
                    book_id,
                    cost,
                    request.form.get('status', 'In')
                ))
                library.save_data()
                flash('Book added successfully!', 'success')
            elif action == 'edit':
                book_id = int(request.form['book_id'])
                kwargs = {}
                if request.form['author']: kwargs['author'] = request.form['author']
                if request.form['title']: kwargs['title'] = request.form['title']
                if request.form['isbn']: kwargs['isbn'] = request.form['isbn']
                if request.form['cost']: kwargs['cost'] = float(request.form['cost'])
                if request.form['status']: kwargs['status'] = request.form['status']
                library.books.edit_book(book_id, **kwargs)
                library.save_data()
                flash('Book edited successfully!', 'success')
            elif action == 'delete':
                book_id = int(request.form['book_id'])
                library.books.delete_book(book_id)
                library.save_data()
                flash('Book deleted successfully!', 'success')
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('manage_books'))
    
    books = list(library.books.books.values())
    return render_template('books.html', books=books)

@app.route('/patrons', methods=['GET', 'POST'])
def manage_patrons():
    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'add':
                patron_id = int(request.form['patron_id'])
                library.patrons.add_patron(Patron(
                    request.form['name'],
                    patron_id,
                    float(request.form.get('fine_balance', 0.0)),
                    int(request.form.get('current_books_out', 0))
                ))
                library.save_data()
                flash('Patron added successfully!', 'success')
            elif action == 'edit':
                patron_id = int(request.form['patron_id'])
                kwargs = {}
                if request.form['name']: kwargs['name'] = request.form['name']
                if request.form['fine_balance']: kwargs['fine_balance'] = float(request.form['fine_balance'])
                if request.form['current_books_out']: kwargs['current_books_out'] = int(request.form['current_books_out'])
                library.patrons.edit_patron(patron_id, **kwargs)
                library.save_data()
                flash('Patron edited successfully!', 'success')
            elif action == 'delete':
                patron_id = int(request.form['patron_id'])
                library.patrons.delete_patron(patron_id)
                library.save_data()
                flash('Patron deleted successfully!', 'success')
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('manage_patrons'))
    
    patrons = list(library.patrons.patrons.values())
    return render_template('patrons.html', patrons=patrons)

@app.route('/loans', methods=['GET', 'POST'])
def manage_loans():
    library.loans.update_loan_status(library.patrons)  # Auto-update statuses
    if request.method == 'POST':
        action = request.form.get('action')
        try:
            if action == 'add':
                loan_id = int(request.form['loan_id'])
                book_id = int(request.form['book_id'])
                patron_id = int(request.form['patron_id'])
                due_date_str = request.form['due_date']  # Expect YYYY-MM-DD
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else datetime.datetime.now() + datetime.timedelta(days=10)
                library.loans.add_loan(Loan(loan_id, book_id, patron_id, due_date))
                library.save_data()
                flash('Loan added successfully!', 'success')
            elif action == 'edit':
                loan_id = int(request.form['loan_id'])
                kwargs = {}
                if request.form['due_date']:
                    kwargs['due_date'] = datetime.datetime.strptime(request.form['due_date'], '%Y-%m-%d')
                if request.form['status']: kwargs['status'] = request.form['status']
                library.loans.edit_loan(loan_id, **kwargs)
                library.save_data()
                flash('Loan edited successfully!', 'success')
            elif action == 'delete':
                loan_id = int(request.form['loan_id'])
                library.loans.delete_loan(loan_id)
                library.save_data()
                flash('Loan deleted successfully!', 'success')
            elif action == 'pay_fines':
                patron_id = int(request.form['patron_id'])
                amount = float(request.form['amount'])
                library.loans.pay_fines(patron_id, amount, library.patrons)
                library.save_data()
                flash('Fines paid successfully!', 'success')
            elif action == 'report_lost':
                loan_id = int(request.form['loan_id'])
                library.loans.report_lost(loan_id, library.patrons, library.books)
                library.save_data()
                flash('Lost book reported successfully!', 'success')
        except ValueError as e:
            flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('manage_loans'))
    
    loans = list(library.loans.loans.values())
    overdue_loans = library.loans.list_overdue_loans()  # But since it's print, adapt if needed
    return render_template('loans.html', loans=loans, overdue_loans=overdue_loans)

if __name__ == '__main__':
    app.run(debug=True)
