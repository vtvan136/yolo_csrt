from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')

BE_HOST = os.getenv('BE_HOST')
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
