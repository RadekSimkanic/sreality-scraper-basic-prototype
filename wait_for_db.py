import psycopg2
import time
from psycopg2 import OperationalError
from utils.config import load_db_configuration


def wait_for_postgres(max_attempts=64, sleep_seconds=5):
    attempts = 0
    db_name, db_user, db_password, db_host, db_port = load_db_configuration()
    while attempts < max_attempts:
        try:
            conn = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.close()
            print("PostgreSQL is ready.")
            return
        except OperationalError as e:
            print(f"PostgreSQL is not ready: {e}")
            attempts += 1
            time.sleep(sleep_seconds)

    print("Failed to connect to PostgreSQL. Aborting the wait.")


wait_for_postgres()
