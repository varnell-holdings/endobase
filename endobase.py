# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
docs = {'rf': 'Feller',
      'cb': 'Bariol',
      'aw': 'Wettstein'}

while True:
    response = input('Doctor:  ')
    if response in docs:
        doctor = docs[response]
        break
print(doctor)
    


docs = {'rf': 'Feller',
      'cb': 'Bariol',
      'aw': 'Wettstein'}