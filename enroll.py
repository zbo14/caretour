from csv import writer
from patient import Patient
from util import read_csv_rows, today

def get_patients():
    rows = read_csv_rows('data.csv')
    fields = rows.pop(0)
    mrn = fields.index('MRN')
    patients = {}
    for row in rows:
        if row[mrn] not in patients:
            patients[row[mrn]] = Patient(fields, row)
        patients[row[mrn]].add_appt(fields, row)
    return patients

# Writes patient enrollment results to csv
def enroll_patients(day = today()):
    fields = ['MRN', 'Name', 'Mobile', 'Email', 'CareTour', 'Location']
    rows = [patient.to_row() for patient in get_patients().values() if patient.enrolled(day)]
    with open('results.csv', 'w') as file:
        w = writer(file)
        w.writerow(fields)
        for row in rows:
            w.writerow(row)

if __name__ == '__main__':
    from datetime import date

    day = date(2018, 4, 15)
    enroll_patients(day)
