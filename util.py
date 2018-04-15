from csv import reader
from datetime import datetime

def is_bronch(type):
    return type == 'FLEX BRONCH WITH BAL' or type == 'TRANS BRONCH BX'

def is_pleurx(type):
    return type == 'PLEURX'

def is_thoracentesis(type):
    return type == 'THORACENTESIS'

def parse_datetime(fields, row):
    date = row[fields.index('Date')]
    time = row[fields.index('Appt Time')]
    return datetime.strptime(date + ' ' + time, '%m/%d/%y %I:%M %p')

def read_csv_rows(filename):
    with open(filename) as file:
        return [row for row in reader(file)]

def today():
    return datetime.now().date()
