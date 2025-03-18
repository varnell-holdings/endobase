# endobase

This program dumps info into endobase from Blue Chip and human input and uploads some of that data to an AWS S3 bucket for use by the docbill program




Installation
============

Minicona3  Windows installer - accept defaults

pip install dependencies

if you get error with pip  re SSL certificates it means the following paths need to be appended to path variable
 ~\Miniconda3  ~\Miniconda3\Scripts   ~\Miniconda3\Library\bin
 can be just temporary if you don't have admin rights


pip install --upgrade boto3

pip install --upgrade pyautogui

install AWS CLI utulity  Windows installer  restart terminal and run aws configure - need info from .aws file

using tillet1957 account at Amazon

endobase.py puts data into the patients.csv file in the dec601 bucket

make 2 directories in ~\Miniconda3

\endobase

\endobase_local

\endobase recieves endobase.py from github which downloads endobase_main.py from aws intp \endobase_local

    
