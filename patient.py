from util import is_bronch, is_pleurx, is_thoracentesis, parse_datetime

class Patient():
    '''
        A patient with personal/contact information, appointment details,
        and enrollment in education program.
    '''

    def __init__(self, fields, row):
        self.id = int(row[fields.index('MRN')])
        self.name = row[fields.index('Patient')]
        self.language = row[fields.index('Pref Language')]
        self.mobile = row[fields.index('Mobile #')]
        self.email = row[fields.index('Pt. E-mail Address')]
        self.appts = {}
        self.upcoming = []
        self.care_tour = None
        self.location = 1

    def to_row(self):
        return [self.id, self.name, self.mobile, self.email, self.care_tour, self.location]

    def add_appt(self, fields, row):
        dt = parse_datetime(fields, row)
        type = row[fields.index('Type')]
        if dt in self.appts:
            raise ValueError('Patient %d already has an appt at %s' % (self.id, dt))
        self.appts[dt] = type

    # Enrolls (or doesn't enroll) the patient in an educational program.
    # Returns a bool indicating whether the patient was enrolled.
    def enrolled(self, day):
        self.care_tour = None
        return self.speaks_english() and \
            self.has_upcoming_appts(day) and \
            self.set_care_tour()

    def single_appt_care_tour(self):
        type = self.appts[self.upcoming[0]]
        if is_bronch(type):
            self.care_tour = 1
        elif is_thoracentesis(type):
            self.care_tour = 3
        elif is_pleurx(type):
            self.care_tour = 4
        else:
            return False
        return True

    def multi_appt_care_tour(self):
        dt1 = self.upcoming[0]
        dt2 = self.upcoming[1]
        type1 = self.appts[dt1]
        type2 = self.appts[dt2]
        if dt1.date() == dt2.date() and \
            (is_bronch(type1) or is_bronch(type2)) and \
            (is_thoracentesis(type1) or is_thoracentesis(type2)):
            self.care_tour = 1
            return True
        return self.single_appt_care_tour()

    # Assigns (or doesn't assign) a care tour to the patient.
    # Returns a bool indicating whether the patient was assigned a care tour.
    def set_care_tour(self):
        if len(self.upcoming) == 1:
            return self.single_appt_care_tour()
        else:
            return self.multi_appt_care_tour()

    def speaks_english(self):
        return self.language == 'English'

    # Returns a bool indicating whether the patient has upcoming appointments at least 2 days away.
    def has_upcoming_appts(self, day):
        self.upcoming = []
        for dt in sorted(self.appts.keys()):
            if (dt.date() - day).days >= 2:
                self.upcoming.append(dt)
        return bool(self.upcoming)

    def __repr__(self):
        return str(vars(self))
