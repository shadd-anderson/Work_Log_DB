import datetime
import os

from peewee import *

db = SqliteDatabase('work_log.db')

DATE_FORMAT = "%m/%d/%y"


class Entry(Model):
    """ Entry class, contains employee, work done (or title), date done, time taken, and any user comments """
    employee = CharField(max_length=255)
    work_done = CharField(max_length=255)
    date = DateField(formats=[DATE_FORMAT], default=datetime.datetime.now())
    time = IntegerField()
    comments = CharField(max_length=255)

    def to_string(self):
        return "{} did {} on {}. Took {} minutes. {}".format(
                self.employee,
                self.work_done,
                datetime.datetime.strptime(self.date, "%Y-%m-%d").strftime(
                    DATE_FORMAT),
                self.time,
                self.comments)

    class Meta:
        database = db


def cls():
    """ Clears the screen """
    os.system('cls' if os.name == 'nt' else 'clear')


def verify_int(prompt):
    """ Verifies input as an integer """
    success = False
    while not success:
        try:
            result = int(input(prompt))
        except ValueError:
            print("Please enter a valid integer...")
        else:
            success = True

    return result


def verify_date(prompt, date_format):
    """ Verifies input as a date with a specified format """
    success = False
    while not success:
        try:
            date = input(prompt)
            if date != '':
                result = datetime.datetime.strptime(date, date_format)
            else:
                result = None
        except ValueError:
            print("Please enter the date in a {} format.".format(user_friendly_date(date_format)))
        else:
            success = True

    return result


def user_friendly_date(date_format):
    """ Takes a python date format and converts it to a more user-friendly string """
    friendly_date = date_format
    friendly_date = friendly_date.replace("%d", "DD")
    friendly_date = friendly_date.replace("%m", "MM")
    friendly_date = friendly_date.replace("%y", "YY")
    friendly_date = friendly_date.replace("%Y", "YYYY")

    return friendly_date


def input_new_entry():
    """ Prompts and creates for new entry """
    employee = input("Please enter the name of the employee: ")
    work_done = input("Please enter the work done: ")
    time = verify_int("Please enter the time in minutes that {} took: ".format(work_done))
    comments = input("Please enter any extra comments (optional): ")
    return Entry(employee=employee,
                 work_done=work_done,
                 time=time,
                 comments=comments)


def add_entry(new_entry):
    Entry.create(
        employee=new_entry.employee,
        work_done=new_entry.work_done,
        time=new_entry.time,
        comments=new_entry.comments
    )


def enter():
    """ Allows for break before moving on """
    input("Please press enter to continue")


def search_entries():
    pass


def main():
    db.connect()
    db.create_tables([Entry], safe=True)

    menu = {1: "Add entry", 2: "Search entries", 3: "Quit"}
    online = True

    while online:
        print("Welcome to the work log! Here's what you can do:")
        for item in menu:
            print("{}. {}".format(item, menu[item]))
        choice = verify_int("Enter the number of which choice you would like: ")

        if choice == 1:
            new_entry = input_new_entry()
            add_entry(new_entry)
            enter()
            cls()

        elif choice == 2:
            search_entries()

        elif choice == 3:
            online = False


if __name__ == '__main__':
    main()
