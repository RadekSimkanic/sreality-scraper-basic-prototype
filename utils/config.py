import os
import configparser


def load_db_configuration():
    """Load database configuration from environment variables or config.ini file."""
    config = configparser.ConfigParser()

    # Define the list of variables
    env_variables = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    ini_variables = ['name', 'user', 'password', 'host', 'port']


    # Loading values from environment
    values = [os.environ.get(var) for var in env_variables]

    # If any value is missing in the environment, load it from the configuration file
    if any(value is None for value in values):
        try:
            config.read('config.ini')

            # Loading values from the configuration file if any are missing in the environment
            values = [config['database'][var] for var in ini_variables]

        except (configparser.NoSectionError, configparser.NoOptionError, FileNotFoundError):
            raise ValueError("Please set the required environment variables or provide a valid config.ini file.")

    # Check if all values are successfully loaded
    if any(value is None for value in values):
        raise ValueError("Please set the required environment variables or provide a valid config.ini file.")

    return tuple(values)


def load_sreality_configuration():
    """Load configuration for Sreality API from the config.ini file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    url = config['sreality_api']['url']
    number_of_items = config['sreality_api']['number_of_items']
    return url, number_of_items
