import csv
from datetime import datetime, timedelta
from tkinter import Tk, N, S, E, W, StringVar, ttk, Menu, FALSE, Toplevel
import webbrowser
from tkcalendar import Calendar
import logging
import os
import os.path
from configparser import ConfigParser


import pyautogui as pya
import boto3
s3 = boto3.resource("s3")

today = datetime.today()
selected_date = None

add = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(add)
endobase_local_path = os.path.join(base, "endobase_local")
staff_file = os.path.join(endobase_local_path, "endobase_staff.ini")
logging_file = os.path.join(endobase_local_path, "logging.txt")
patient_list_file = os.path.join(endobase_local_path, "patients.csv")

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(logging_file), logging.StreamHandler()],
    format="%(asctime)s %(message)s",
)

try:
    s3.Object("dec601", "endobase_staff.ini").download_file(staff_file)
except Exception as e:
    logging.info(f"Failed to get staff file from AWS  {e}")
    pass

config_parser = ConfigParser(allow_no_value=True)
config_parser.read(staff_file)


ENDOSCOPISTS = config_parser.options("ENDOSCOPISTS")
ENDOSCOPISTS = [a.title() for a in ENDOSCOPISTS]
ANAESTHETISTS = config_parser.options("ANAESTHETISTS")
ANAESTHETISTS = [a.title() for a in ANAESTHETISTS]

PROCEDURES = [
    "None",
    "Double",
    "Colonoscopy",
    "Gastroscopy",
    "Flexible Sigmoidoscopy",
]


def open_roster():
    webbrowser.open("http://dec601.nfshost.com/deccal.html")


def upload_aws(data):
    """Get the aws patients file. Delete old entries.
    Add the new data & upload."""

    s3.Object("dec601", "patients.csv").download_file(patient_list_file)

    # put aws data into temp list & remove old data
    temp_list = []
    with open(patient_list_file, encoding="utf-8") as h:
        reader = csv.reader(h)
        for pat in reader:
            try:
                pat_date = datetime.strptime(pat[0], "%d/%m/%Y")
                if pat_date + timedelta(days=12) >= today:
                    temp_list.append(pat)
            except Exception as e:
                logging.info(f"Failed to read patient data from aws list {e}")

    temp_list.append(data)

    # write the temp list over the old aws file
    with open(patient_list_file, "w", encoding="utf-8") as h:
        csv_writer = csv.writer(h, dialect="excel", lineterminator="\n")
        for p in temp_list:
            csv_writer.writerow(p)

    # upload aws file
    try:
        with open(patient_list_file, "rb") as data:
            s3.Bucket("dec601").put_object(Key="patients.csv", Body=data)
    except Exception as e:
        logging.info(f"Failed to upload to AWS  {e}")

    try:
        os.remove(patient_list_file)
    except Exception as e:
        logging.info(f"Failed to remove aws_file  {e}")


def clicks(procedure, record_number, endoscopist, anaesthetist):
    """
    Workhorse pyautogui function. Tabs through endobase add patient entry page
     and inputs data
    """
    pya.click(250, 50)
    pya.PAUSE = 0.5
    pya.hotkey("alt", "a")
    pya.typewrite(["tab"] * 1)
    pya.typewrite(procedure)
    pya.press("enter")
    pya.typewrite(["tab"] * 5)
    pya.typewrite(record_number)
    pya.press("enter")
    pya.typewrite(["tab"] * 6)
    pya.typewrite(endoscopist)
    pya.press("enter")
    pya.press("tab")
    pya.typewrite(anaesthetist)
    pya.press("enter")

    pya.hotkey("alt", "o")
    pya.click(1000, 230)


class DatePickerWindow:
    def __init__(self, parent, callback):
        self.parent = parent
        self.callback = callback

        # Create a new top-level window
        self.top = Toplevel(parent)
        self.top.title("Select List Date")

        # Make it modal (will block interaction with the parent window)
        self.top.transient(parent)
        self.top.grab_set()

        # Position it near the parent window
        x = parent.winfo_rootx() + 50
        y = parent.winfo_rooty() + 350
        self.top.geometry(f"+{x}+{y}")

        # Create the calendar widget
        today = datetime.now()
        self.cal = Calendar(
            self.top,
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
            showweeknumbers=False,
            showothermonthdays=False,
            foreground="black"
        )
        self.cal.pack(padx=10, pady=10)

        # Add a select button
        select_btn = ttk.Button(self.top, text="Select", command=self.select_date)
        select_btn.pack(pady=5)

        # Add a cancel button
        cancel_btn = ttk.Button(self.top, text="Cancel", command=self.top.destroy)
        cancel_btn.pack(pady=5)

    def select_date(self):
        # Get the selected date as datetime object
        global selected_date
        selected_date = self.cal.selection_get()

        # Call the callback function with the selected date
        self.callback(selected_date)

        # Close the window
        self.top.destroy()


# Function to receive the selected date from the picker
def on_date_selected(date):
    print_date = date.strftime("%d-%m-%Y")
    date_label["text"] = print_date


def button_enable(*args):
    """Toggle Send button when all data entered"""
    global selected_date
    endoscopist = endo.get()
    anaesthetist = anaes.get()
    record_number = mrn.get()
    procedure = proc.get()
    if all({endoscopist, anaesthetist, record_number, procedure, selected_date}):
        but.config(state="normal")
        but_text.set("Send!")
        root.update_idletasks()
        return


def runner(*args):
    """
    Main function that runs when button clicked
    gets data from gui, does a few checks,
    then fires off clicks() function.
    Then uploads data for docbill checking.
    """
    global selected_date
    endoscopist = endo.get()
    anaesthetist = anaes.get()
    record_number = mrn.get()
    procedure = proc.get()


    if procedure != "Double":
        double_flag = "False"
        clicks(procedure, record_number, endoscopist, anaesthetist)
    else:
        double_flag = "True"
        clicks("Gastroscopy", record_number, endoscopist, anaesthetist)
        clicks("Colonoscopy", record_number, endoscopist, anaesthetist)

    data = [
        selected_date.strftime("%d/%m/%Y"),
        record_number,
        endoscopist,
        double_flag,
    ]

    upload_aws(data)

    # configure gui for next run
    proc.set("")
    mrn.set("")
    but_text.set("Next patient")
    but.config(state="disabled")
    # pya.click(root.winfo_x() + 250, root.winfo_y() + 150)
    mr.focus()


# set up gui
root = Tk()
root.title("Endobase Data Entry")
root.geometry("360x280+1400+250")
root.option_add("*tearOff", FALSE)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

menubar = Menu(root)
root.config(menu=menubar)
# win['menu'] = menubar
menu_extras = Menu(menubar)
# menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_extras, label="Extras")
menu_extras.add_command(label="Roster", command=open_roster)
# menu_extras.add_command(label='Web Page', command=open_today)


endo = StringVar()
endo.trace("w", button_enable)
anaes = StringVar()
anaes.trace("w", button_enable)
mrn = StringVar()
mrn.trace("w", button_enable)
proc = StringVar()
proc.trace("w", button_enable)
but_text = StringVar()


open_picker_btn = ttk.Button(
    mainframe,
    text="Select Date",
    command=lambda: DatePickerWindow(mainframe, on_date_selected),
)
open_picker_btn.grid(column=1, row=1, sticky=W)

# Label to show the selected date
date_label = ttk.Label(mainframe, text="No date selected")
date_label.grid(column=2, row=1, sticky=W)


ttk.Label(mainframe, text="Endoscopist").grid(column=1, row=2, sticky=W)
end = ttk.Combobox(mainframe, textvariable=endo)
end["values"] = ENDOSCOPISTS
end["state"] = "readonly"
end.grid(column=2, row=2, sticky=W)

ttk.Label(mainframe, text="Anaesthetist").grid(column=1, row=3, sticky=W)
an = ttk.Combobox(mainframe, textvariable=anaes)
an["values"] = ANAESTHETISTS
an["state"] = "readonly"
an.grid(column=2, row=3, sticky=W)

ttk.Label(mainframe, text="MRN").grid(column=1, row=4, sticky=W)
mr = ttk.Entry(mainframe, textvariable=mrn)
mr.grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, text="Procedure").grid(column=1, row=5, sticky=W)
pr = ttk.Combobox(mainframe, textvariable=proc)
pr["values"] = PROCEDURES
pr["state"] = "readonly"
pr.grid(column=2, row=5, sticky=W)

but = ttk.Button(mainframe, textvariable=but_text, command=runner)
but_text.set("")
but.grid(column=2, row=6, sticky=W)
but.config(state="disabled")


root.bind("<Return>", runner)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

proc.set("")
mrn.set("")
open_picker_btn.focus()

root.attributes("-topmost", True)
root.mainloop()
