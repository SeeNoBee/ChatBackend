# Конфиг для токенов
import os

from dotenv import load_dotenv

load_dotenv()


class UtilsConfig:
    secret_token = os.getenv('secret_token')
