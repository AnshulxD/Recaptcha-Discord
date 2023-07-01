from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Secrets:
    # Google ReCaptcha Config, https://developers.google.com/recaptcha
    site_key: str = getenv("SITE_KEY")
    site_secret_key: str = getenv("SITE_SECRET_KEY")

    # MySQL Config
    db_host: str = getenv("DB_HOST")
    db_port: str = getenv("DB_PORT")
    db_user: str = getenv("DB_USER")
    db_passwd: str = getenv("DB_PASSWD")
    db_name: str = getenv("DB_NAME")
