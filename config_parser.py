import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
TOKEN = config["settings"]["TOKEN"]
ADMINS = [int(admin) for admin in config["settings"]["admins"].split(",")]
WKHTMLTOPDF_PATH = config["settings"]["WKHTMLTOPDF_PATH"]


class DB:
    user = config["db"]["user"]
    password = config["db"]["password"]
    database = config["db"]["database"]
    host = config["db"]["host"]
    port = config["db"]["port"]
