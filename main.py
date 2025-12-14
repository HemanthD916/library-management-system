from library import Library

def main_menu():
    library = Library()
    while True:
        choice = input("Library Management System\n1. Manage Books\n2. Manage Patrons\n3. Manage Loans\n4. Exit\nPlease enter a number from above: ")
        if choice == '1':
            library.manage_books()
        elif choice == '2':
            library.manage_patrons()
        elif choice == '3':
            library.manage_loans()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()