import os
import sys
import toml
import logging

default_configuration = {
    "telegram": {
        "bot_name": "your_bot_@_username",
        "api_key": "your_telegram_api_key",
        "worker_count": 20,
        "admin": "hexatester",
        "max_inline": 10,
    },
    "language": {"default": "English"},
    "database": {
        "sql_uri": "sqlite://",
        "postgres": True,
        "connection_count": 20,
        "overflow_count": 10,
    },
    "logging": {
        "sentry_enabled": False,
        "sentry_token": "",
        "log_level": logging.INFO,
        "debug": False,
    },
    "webhook": {
        "enabled": False,
        "domain": "https://localhost",
        "token": "pollbot",
        "cert_path": "/path/to/cert.pem",
        "port": 7000,
    },
}

config_path = os.path.expanduser("~/.config/klassbot.toml")

if not os.path.exists(config_path):
    with open(config_path, "w") as file_descriptor:
        toml.dump(default_configuration, file_descriptor)
    print(
        "Please adjust the configuration file at '~/.config/klassbot.toml'"
    )
    sys.exit(1)
else:
    config = toml.load(config_path)
