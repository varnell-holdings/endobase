# -*- coding: utf-8 -*-
"""
Data entry for endobase.
"""


import csv
from datetime import datetime as dt
from collections import defaultdict
import time
from tkinter import Tk, N, S, E, W, StringVar, ttk, Menu, FALSE
import webbrowser

import pyautogui as pya
import pyperclip


ANAESTHETISTS = ['Bowring',
                 'Brown',
                 'Doherty',
                 'Locum',
                 'Manasiev',
                 'MOYLE',
                 "O'Hare",
                 "O'Neill",
                 "O'Sullivan",
                 'Riley',
                 'Robertson',
                 'Steele',
                 'Stevens',
                 'Stone',
                 'Tester',
                 'Thompson',
                 'Tillett',
                 'Vuong',
                 'Wood']

ENDOSCOPISTS = ['Bariol',
                'Danta',
                'Feller',
                'GETT',
                'GHALY',
                'LORD',
                'Meagher',
                'Stoita',
                'Vickers',
                'Vivekanandarajah',
                'Wettstein',
                'Williams',
                'DE LUCA',
                'Owen',
                'Bye',
                'Kim',
                'Haiffer',
                'Mill',
                'NGUYEN',
                'Sanagapalli',
                'Wu']

PROCEDURES = ['None',
              'Double',
              'Colonoscopy',
              'Gastroscopy',
              'Oesophageal Dilatation',
              'Flexible Sigmoidoscopy',
              'BRAVO',
              'HALO']


def patient_to_file(data):
    """
    input data is a tuple containing
    date, doctor, ,mrn, name
    """
    with open('patients.csv', 'wt') as f:
        writer = csv.writer(f)
        writer.writerow(data)
	
			  
			  

def clicks(procedure, record_number, endoscopist, anaesthetist):
    pya.click(250, 50)
    pya.PAUSE = 0.5
    pya.hotkey('alt', 'a')
    pya.typewrite(['tab'] * 1)
    pya.typewrite(procedure)
    pya.press('enter')
    pya.typewrite(['tab'] * 5)
    pya.typewrite(record_number)
    pya.press('enter')
    time.sleep(1)
    pya.hotkey('shift', 'tab')
    pya.hotkey('shift', 'tab')	
    pya.hotkey('shift', 'tab')
    pya.hotkey('ctrl', 'c')
    pya.hotkey('shift', 'tab')
    pya.hotkey('ctrl', 'c')
    pya.typewrite(['tab'] * 10)
    pya.typewrite(endoscopist)
    pya.press('enter')
    pya.press('tab')
    pya.typewrite(anaesthetist)
    pya.press('enter')
    pya.hotkey('alt', 'o')
    pya.click(1000, 230)


def open_roster():
    webbrowser.open('www.home.aone.net.au/tillett/dec/roster.html')


def runner(*args):
    global type_of_procedures
    endoscopist = endo.get()
    anaesthetist = anaes.get()
    record_number = mrn.get()
    procedure = proc.get()
    proc.set('None')
    mrn.set('')
    mr.focus()

    no_doc = endoscopist not in ENDOSCOPISTS
    no_an = anaesthetist not in ANAESTHETISTS
    if procedure == 'None' or no_doc or no_an:
        pya.alert(text='Missing Data!',
                  title='',
                  button='OK')
        raise Exception

    if not record_number.isdigit() or int(record_number) > 300000:
        pya.alert(text='MRN looks wrong!',
                  title='',
                  button='OK')
        raise Exception

    ignore_number_flag = False
    if procedure in type_of_procedures[record_number]:
        reply = pya.confirm(
            text='You already made a {} for this patient.'.format(procedure),
            title='',
            buttons=['Continue', 'Cancel'])
        if reply == 'Cancel':
            raise Exception
        else:
            ignore_number_flag = True

    if procedure == 'Double':
        type_of_procedures[record_number].extend(
            ['Colonoscopy', 'Gastroscopy'])
    else:
        type_of_procedures[record_number].append(procedure)
    print(type_of_procedures[record_number])

    number_of_procedures = len(type_of_procedures[record_number])

    print(number_of_procedures)
    if number_of_procedures > 2 and not ignore_number_flag:
        reply = pya.confirm(
            text='Do you want {} procedures for this patient??'.format(
                number_of_procedures),
            title='',
            buttons=['Yes', 'No'])
        if reply == 'No':
            raise Exception

    print(endoscopist + '-' + anaesthetist +
          '-' + procedure + '-' + record_number)
	
    print(__file__)
    print("HULLO")
    if procedure == 'Double':
        double_flag = True
        procedure = 'Gastroscopy'
    else:
        double_flag = False

    clicks(procedure, record_number, endoscopist, anaesthetist)

    data = ('22/04/2020', endoscopist, record_number, 'BillSmith')
    patient_to_file(data)

    if double_flag:
        procedure = 'Colonoscopy'
        clicks(procedure, record_number, endoscopist, anaesthetist)

# set up gui


root = Tk()
root.title('Endobase Data Entry')
root.geometry('320x190+900+100')
root.option_add('*tearOff', FALSE)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

menubar = Menu(root)
root.config(menu=menubar)
# win['menu'] = menubar
menu_extras = Menu(menubar)
# menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_extras, label='Extras')
menu_extras.add_command(label='Roster', command=open_roster)
# menu_extras.add_command(label='Web Page', command=open_today)


endo = StringVar()
anaes = StringVar()
mrn = StringVar()
proc = StringVar()

type_of_procedures = defaultdict(list)

ttk.Label(mainframe, text="Endoscopist").grid(column=1, row=1, sticky=W)
end = ttk.Combobox(mainframe, textvariable=endo)
end['values'] = ENDOSCOPISTS
end['state'] = 'readonly'
end.grid(column=2, row=1, sticky=W)

ttk.Label(mainframe, text="Anaesthetist").grid(column=1, row=2, sticky=W)
an = ttk.Combobox(mainframe, textvariable=anaes)
an['values'] = ANAESTHETISTS
an['state'] = 'readonly'
an.grid(column=2, row=2, sticky=W)

ttk.Label(mainframe, text="MRN").grid(column=1, row=3, sticky=W)
mr = ttk.Entry(mainframe, textvariable=mrn)
mr.grid(column=2, row=3, sticky=W)

ttk.Label(mainframe, text="Procedure").grid(column=1, row=4, sticky=W)
pr = ttk.Combobox(mainframe, textvariable=proc)
pr['values'] = PROCEDURES
pr['state'] = 'readonly'
pr.grid(column=2, row=4, sticky=W)

but = ttk.Button(mainframe, text='Send!', command=runner)
but.grid(column=2, row=5, sticky=E)
but.bind('<Return>', runner)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

end.focus()
proc.set('None')
root.attributes("-topmost", True)

root.mainloop()
