import unittest
from patient import Patient

class TestPatient(unittest.TestCase):

    def setUp(self):
        from datetime import date

        self.day = date(2018, 2, 1)
        self.appt_fields = ['Date', 'Appt Time', 'Type']
        self.patient_fields = ['MRN', 'Patient', 'Pref Language', 'Mobile #', 'Pt. E-mail Address']
        self.patient = Patient(self.patient_fields, [1445578838, 'patient_name', 'English', '333-333-3333', 'patient_email@gmail.com'])

    def reset_appts(self):
        self.patient.appts = {}

    def test_non_english_speaking_patient(self):
        self.patient.language = 'French'
        assert not self.patient.enrolled(self.day)
        assert self.patient.care_tour == None
        self.patient.language = 'English'

    def test_patient_with_past_appt(self):
        self.patient.add_appt(self.appt_fields, ['1/20/18', '9:00 AM', 'THORACENTESIS'])
        assert not self.patient.enrolled(self.day)
        assert self.patient.care_tour == None

    def test_patient_with_appt_tmrw(self):
        self.patient.add_appt(self.appt_fields, ['2/2/18', '10:00 AM', 'PLEURX'])
        assert not self.patient.enrolled(self.day)
        assert self.patient.care_tour == None
        self.reset_appts()

    def test_patient_with_appt(self):
        self.patient.add_appt(self.appt_fields, ['2/3/18', '10:00 AM', 'FLEX BRONCH WITH BAL'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 1
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '11:00 AM', 'TRANS BRONCH BX'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 1
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '12:00 PM', 'THORACENTESIS'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 3
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '1:00 PM', 'PLEURX'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 4
        self.reset_appts()

    def test_patient_with_same_day_appts(self):
        self.patient.add_appt(self.appt_fields, ['2/3/18', '9:00 AM', 'THORACENTESIS'])
        self.patient.add_appt(self.appt_fields, ['2/3/18', '10:00 AM', 'FLEX BRONCH WITH BAL'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 1
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '9:00 AM', 'TRANS BRONCH BX'])
        self.patient.add_appt(self.appt_fields, ['2/3/18', '10:00 AM', 'PLEURX'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 1
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '9:00 AM', 'THORACENTESIS'])
        self.patient.add_appt(self.appt_fields, ['2/3/18', '10:00 AM', 'PLEURX'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 3
        self.reset_appts()

        self.patient.add_appt(self.appt_fields, ['2/3/18', '9:00 AM', 'PLEURX'])
        self.patient.add_appt(self.appt_fields, ['2/3/18', '10:00 AM', 'FLEX BRONCH WITH BAL'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 4
        self.reset_appts()

    def test_patient_with_diff_day_appts(self):
        self.patient.add_appt(self.appt_fields, ['2/3/18', '9:00 AM', 'THORACENTESIS'])
        self.patient.add_appt(self.appt_fields, ['2/4/18', '8:00 AM', 'FLEX BRONCH WITH BAL'])
        assert self.patient.enrolled(self.day)
        assert self.patient.care_tour == 3
        self.reset_appts()

if __name__ == '__main__':
    unittest.main()
