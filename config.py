from configparser import ConfigParser


def load_config(path: str = "config.ini") -> ConfigParser:
    """ Loads config.ini
        path - str = "config.ini"
        Example:
        TOKEN = load_config().get("Bot", "Token")
    """
    config = ConfigParser()
    config.read(path)
    return config