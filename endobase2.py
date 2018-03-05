# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyautogui as pya
import pyperclip
import time


DOCTORS = {'cb': 'Dr C Bariol',
           'md': 'DR M Danta',
           'rf': 'Dr R Feller',
           'rg': 'DR R Gett',
           'sg': 'Dr S Ghaly',
           'rl': 'Prof R Lord',
           'am': 'Dr A Meagher',
           'as': 'Dr A Stoita',
           'cv': 'Dr C Vickers',
           'sv': 'Dr S Vivekanandarajah',
           'aw': 'Dr A Wettstein',
           'dw': 'Dr D Williams',
           'go': 'Dr G Owen',
           'wb': 'Dr W Bye',
           'bb': 'Dr W Bye',
           'vn': 'Dr V Nguyen',
           'jm': 'Dr J Mill',
           'cw': 'Dr Yang Wu',
           'ak': 'Dr A Kim',
           'ndl': 'Dr N De Luca'}

ANAESTHETISTS = {'tt': 'Dr T Thompson',
                 'sv': 'Dr S Vuong',
                 'cb': 'Dr C Brown',
                 'jr': 'Dr J Riley',
                 'js': 'Dr J Stevens',
                 'db': 'Dr D Bowring',
                 'gos': "Dr G O'Sullivan",
                 'jt': 'Dr J Tester',
                 'rw': 'Dr Rebecca Wood',
                 'mm': 'Dr M Moyle',
                 'mon': "Dr Martine O'Neill",
                 'ni': 'Dr N Ignatenko',
                 'ns': 'Dr N Steele',
                 'tr': 'Dr Timothy Robertson',
                 'ms': 'Dr M Stone',
                 'fd': 'Dr Felicity Doherty',
                 'bm': 'Dr B Manasiev',
                 'eoh': "Dr E O'Hare",
                 'locum': 'locum',
                 'jrt': 'Dr J Tillett'}

PROCEDURES = {'p': 'Gastroscopy',
               'c': 'Colonoscopy'}

def get_doctor():
    while True:
        doctor = input('Doctor initials: ').lower().strip()
        if doctor in DOCTORS:
            doctor = DOCTORS[doctor]
            print(doctor)
            break
    return doctor
def get_anaesthetist():
    while True:
        anaesthetist = input('Anaesthetist initials: ').lower().strip()
        if anaesthetist in ANAESTHETISTS:
            anaesthetist = ANAESTHETISTS[anaesthetist]
            print(anaesthetist)
            break
    return anaesthetist
def get_mrn():
    while True:
        mrn = input('MRN: ').strip()
        if mrn.isdigit():
            break
    return mrn
def get_procedure():
    while True:
        procedure = input('p or c: ').lower().strip()
        if procedure in {'p', 'c'}:
            procedure = PROCEDURES[procedure]
            break
    return procedure
    
def endobase_write(doctor, anaesthetist, mrn, procedure):
    pya.PAUSE = 1
    pya.click(2500, 50)
    pya.PAUSE = 1
    pya.hotkey('alt', 'a')			
    pya.typewrite(['tab'] * 1)
    pya.typewrite(procedure)
    pya.typewrite(['enter'] * 2)
    
def main():
    doctor = get_doctor()
    anaesthetist = get_anaesthetist()
    mrn = get_mrn()
    procedure = get_procedure()
    endobase_write(doctor, anaesthetist, mrn, procedure)
    
    
    
    
    

if __name__ == '__main__':
    main()
    