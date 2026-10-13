import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_NAME = os.environ.get("DB_NAME", "moviesdb")


def get_connection():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname=DB_NAME,
            )
            return conn
        except psycopg2.OperationalError as e:
            print(f"БД ещё не готова, ждём... (осталось попыток:{retries})")
            retries -= 1
            time.sleep(3)
    raise RuntimeError("Не удалось подключиться к БД")


@app.route("/movies", methods=["GET"])
def list_movies():
    conn = get_connection()

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM movies ORDER BY id;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(rows)


@app.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()

    title = data["title"]
    year = data["year"]
    genre = data["genre"]

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO movies (title, year, genre) VALUES (%s, %s, %s) RETURNING id;",
        (title, year, genre)
    )
    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"status": "ok", "id": new_id}), 201
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)