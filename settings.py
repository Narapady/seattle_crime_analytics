import os

from dotenv import load_dotenv

load_dotenv()

APP_TOKEN = os.getenv("APP_TOKEN")
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
