"""config_test.py"""
import boto3
import os.path
# s3 = boto3.resource('s3')

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

from configparser import ConfigParser



add = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(add)
endobase_local_path = os.path.join(base, "endobase_local")


# aws_file = os.path.join(endobase_local_path, 'patients.csv')
# backup_pat_file = os.path.join(endobase_local_path, 'backup_patients.csv')
# screenshot_for_ocr = os.path.join(endobase_local_path, 'final_screenshot.png')
# logging_file = os.path.join(endobase_local_path, 'logging.txt')

# # next line needs to be added
staff_file = os.path.join(endobase_local_path, 'endobase_staff.ini')
print(str(staff_file))
#  put the following after file statements around line 95
 
# s3.Object('dec601', 'endobase_staff.ini').download_file(staff_file)
s3 = boto3.client('s3')
try:
    # s3.download_file('dec601', 'endobase_staff.ini', 'staff_file')
    with open(staff_file, 'wb') as f:
        s3.download_fileobj('dec601', 'endobase_staff.ini', f)
except:
    pass

config_parser = ConfigParser(allow_no_value=True)
config_parser.read(staff_file)

ENDOSCOPISTS = config_parser.options("ENDOSCOPISTS")
ENDOSCOPISTS = [a.title() for a in ENDOSCOPISTS]
ANAESTHETISTS = config_parser.options("ANAESTHETISTS")
ANAESTHETISTS = [a.title() for a in ANAESTHETISTS]


print(ENDOSCOPISTS)
print(ANAESTHETISTS)


""" add the lines 10, 25,30-43 into endobase.py"""
