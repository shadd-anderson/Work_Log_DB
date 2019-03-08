import datetime
import os

from peewee import *

db = SqliteDatabase('work_log.db')

DATE_FORMAT = "%m/%d/%y"


class Entry(Model):
    """ Entry class, contains employee, work done (or title), date done, time taken, and any user comments """
    employee = CharField(max_length=255, unique=True)
    work_done = CharField(max_length=255)
    date = DateField(formats=[DATE_FORMAT])
    time = IntegerField()
    comments = CharField(max_length=255, default="")

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


def main():
    db.connect()
    db.create_tables([Entry], safe=True)

    shadd = Entry.create(employee="Shadd Anderson",
                         work_done="Did some coding",
                         date="03/06/19",
                         time=120,
                         comments="Set up database and entered a test entry")

    print(Entry.select().get().to_string())
    print(type(shadd.date))


if __name__ == '__main__':
    main()
