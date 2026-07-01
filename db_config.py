from configparser import ConfigParser
from functools import lru_cache
from pathlib import Path

import mysql.connector


DEFAULT_DB_CONFIG = {
    "host": "localhost",
    "username": "root",
    "password": "",
    "database": "facerecognition_att",
}


@lru_cache(maxsize=1)
def get_db_config():
    config = DEFAULT_DB_CONFIG.copy()
    config_path = Path(__file__).with_name("config.ini")

    parser = ConfigParser()
    if config_path.exists():
        parser.read(config_path, encoding="utf-8")
        if parser.has_section("mysql"):
            mysql_section = parser["mysql"]
            for key in config:
                config[key] = mysql_section.get(key, config[key])

    return config


def get_db_connection():
    return mysql.connector.connect(**get_db_config())