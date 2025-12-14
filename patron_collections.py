from patron import Patron

class PatronCollections:
    def __init__(self):
        self.patrons = {}

    def add_patron(self, patron):
        self.patrons[patron.id_number] = patron

    def edit_patron(self, id_number, **kwargs):
        if id_number in self.patrons:
            for key, value in kwargs.items():
                if value.strip():
                    if key == 'fine_balance':
                        try:
                            value = float(value)
                        except ValueError:
                            print("Invalid fine balance; skipping.")
                            continue
                    elif key == 'current_books_out':
                        try:
                            value = int(value)
                        except ValueError:
                            print("Invalid books out; skipping.")
                            continue
                    setattr(self.patrons[id_number], key, value)

    def delete_patron(self, id_number):
        if id_number in self.patrons:
            del self.patrons[id_number]

    def find_patron(self, id_number):
        return self.patrons.get(id_number)

    def list_patrons(self):
        for patron in self.patrons.values():
            print(patron)

    def get_all_patrons(self):
        return {k: vars(v) for k, v in self.patrons.items()}

    def load_patrons(self, patrons):
        self.patrons = {int(k): Patron(**v) for k, v in patrons.items()}

    def manage_patrons(self):
        while True:
            choice = input("Manage Patrons\n1. Add\n2. Edit\n3. Delete\n4. Find\n5. List\n6. Back\nEnter choice: ")
            if choice == '1':
                try:
                    self.add_patron(Patron(input("Name: "), int(input("Patron ID (numbers only): "))))
                except ValueError:
                    print("Invalid ID; try again.")
            elif choice == '2':
                id_number = int(input("Patron ID (numbers only): "))
                print("Leave blank to keep current value.")
                self.edit_patron(id_number, name=input("New name: "), fine_balance=input("New fine balance: $"), 
                                 current_books_out=input("New books out: "))
            elif choice == '3':
                self.delete_patron(int(input("Patron ID (numbers only): ")))
            elif choice == '4':
                print(self.find_patron(int(input("Patron ID (numbers only): "))))
            elif choice == '5':
                self.list_patrons()
            elif choice == '6':
                break