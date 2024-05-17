"""config_test.py"""

from configparser import ConfigParser



add = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(add)
endobase_local_path = os.path.join(base, "endobase_local")


aws_file = os.path.join(endobase_local_path, 'patients.csv')
backup_pat_file = os.path.join(endobase_local_path, 'backup_patients.csv')
screenshot_for_ocr = os.path.join(endobase_local_path, 'final_screenshot.png')
logging_file = os.path.join(endobase_local_path, 'logging.txt')
staff_file = os.path.join(endobase_local_path, 'endobase_staff.ini')


s3 = boto3.resource('s3')  
s3.Object('dec601', 'endobase_staff.ini').download_file(staff_file)


config_parser = ConfigParser(allow_no_value=True)
config_parser.read(staff_file)


ENDOSCOPISTS = config_parser.options("endoscopists")
ENDOSCOPISTS = [a.title() for a in ENDOSCOPISTS]
ANAESTHETISTS = config_parser.options("anaesthetists")
ANAESTHETISTS = [a.title() for a in ANAESTHETISTS]
