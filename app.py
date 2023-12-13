import time
import psycopg2
from flask import Flask, render_template
from utils.config import load_db_configuration

app = Flask(__name__)


def connect_to_database(timeout: float = 60.):
    db_name, db_user, db_password, db_host, db_port = load_db_configuration()
    start_time = time.time()
    while True:
        try:
            # Připojení k databázi
            conn = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            return conn
        except psycopg2.OperationalError as e:
            if time.time() - start_time >= timeout:
                raise
            print(f"Failed to connect to the database. Retrying in 5 seconds. Error: {e}")
            time.sleep(5)


conn = connect_to_database()
cur = conn.cursor()

# Last 500 items from DB table
cur.execute("SELECT title, images FROM flats ORDER BY id DESC LIMIT 500")
scraped_items = [{"title": row[0], "images": row[1].split(";")} for row in cur.fetchall()]

# Close DB connection
cur.close()
conn.close()

# Endpoint
@app.route('/')
def index():
    return render_template('index.html', items=scraped_items)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
