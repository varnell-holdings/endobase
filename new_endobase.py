"""
Easy data entry for Endobase.
Also uploads data to an AWS bucket for use by docbill
program on anaesthetist's computers for error checking.
This just loads the main program from AWS then imports
it from endobase_local
"""
#  uncomment code wnen installing

import logging
import os
import os.path
import sys

# import boto3


add = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(add)
endobase_local_path = os.path.join(base, "endobase_local")
staff_file = os.path.join(endobase_local_path, "endobase_staff.ini")


logging_file = os.path.join(endobase_local_path, "logging.txt")

program_file = os.path.join(endobase_local_path, "endobase_main.py")

sys.path.append(endobase_local_path)


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(logging_file), logging.StreamHandler()],
    format="%(asctime)s %(message)s",
)


# s3 = boto3.resource("s3")


# try:
#     s3.Object("dec601", "endobase_main.py").download_file(program_file)
# except Exception as e:
#     logging.info(f"Failed to get endobase_main.py file from AWS  {e}")
#     pass


import endobase_main
