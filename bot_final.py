import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value.isalpha():
            print("Name must contain only letters.")
        else:
            super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            print("Invalid phone number. It should contain 10 digits.")
        else:
            super().__init__(value)
            
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(birthday)
        except ValueError:
            print("Invalid date format. Please enter the date in DD.MM.YYYY format.")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        new_phone = Phone(phone_number)
        if new_phone.value:
            self.phones.append(new_phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        name_of_record = record.name.value
        self.data[name_of_record] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        if name in self.data:
            return self.data[name]

    def get_birthdays_per_week(self):
        birthdays_per_day = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        today = datetime.date.today()
        for record in self.data.values():
            name = record.name.value
            birthday = record.birthday.value if record.birthday else None
            if birthday:
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                if delta_days < 7:
                    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Monday", "Monday"][birthday_this_year.weekday()]
                    birthdays_per_day[day_of_week].append(name)
        result = []
        for day_of_week, names in sorted(birthdays_per_day.items()):
            if names:
                result.append(f"{day_of_week}: {', '.join(names)}")
        return result

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Oops, something's wrong with the input."
        except KeyError:
            return "Hmm, can't find that contact."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, address_book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, address_book):
    name, phone = args
    record = address_book.find(name)
    if record:
        record.phones[0].value = phone  
        return "Contact updated."
    else:
        return "Contact does not exist."

@input_error
def get_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    else:
        return "Contact does not exist."

@input_error
def add_birthday(args, address_book):
    name, birthday = args
    record = address_book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact does not exist."

@input_error
def show_birthday(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    else:
        return "Birthday information is not available."

def get_all_contacts(address_book):
    result = "List of contacts:\n"
    for name, record in address_book.data.items():
        result += f"{name}: {', '.join(phone.value for phone in record.phones)}"
        if record.birthday:
            result += f", Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
        result += "\n"
    return result

@input_error
def get_birthdays(address_book):
    birthdays = address_book.get_birthdays_per_week()
    if birthdays:
        return "\n".join(birthdays)
    else:
        return "No birthdays in the next week."

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) != 2:
                print("Oops, I need a name and a phone number.")
            else:
                print(add_contact(args, address_book))
        elif command == "change":
            if len(args) != 2:
                print("Oops, I need a name and a phone number.")
            else:
                print(change_contact(args, address_book))
        elif command == "phone":
            if len(args) != 1:
                print("Oops, I need a name.")
            else:
                print(get_phone(args, address_book))
        elif command == "all":
            print(get_all_contacts(address_book))
        elif command == "add-birthday":
            if len(args) != 2:
                print("Oops, I need a name and a birthday.")
            else:
                print(add_birthday(args, address_book))
        elif command == "show-birthday":
            if len(args) != 1:
                print("Oops, I need a name.")
            else:
                print(show_birthday(args, address_book))
        elif command == "birthdays":
            print(get_birthdays(address_book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()