import os
from pathlib import Path


email_from = os.environ.get('email_from')
email_to = os.environ.get('email_to')
email_login = os.environ.get('email_login')
email_pass = os.environ.get('email_pass')
email_to_juridical = os.environ.get('email_to_juridical')
email_to_individual = os.environ.get('email_to_individual')
BASE_DIR = Path(__file__).resolve().parent.parent
INTERNAL_DIR = os.path.join(BASE_DIR, 'sed')