import os
import psycopg2
from flask import Flask, render_template, request

# Very basic parameterized query used to demonstrate the dangers of SQL injection
SEARCH_MAKE_QUERY = "SELECT make, model, price FROM cars WHERE make LIKE '%{make}%';"


server = Flask(__name__)


def search_db(query):
    # TODO: Wrap this in a context manager
    pg_conn = psycopg2.connect(
        host='127.0.0.1',
        dbname=os.environ['pg_db'],
        user=os.environ['pg_user'],
        password=os.environ['pg_pwd'])

    cur = pg_conn.cursor()

    cur.execute(SEARCH_MAKE_QUERY.format(make=query))

    return cur.fetchall()


@server.route('/')
def landing_page():
    query = request.args.get('search')
    search_results = search_db(query) if query else None

    return render_template(
        'base.html',
        search_results=search_results)


server.run('127.0.0.1', 8080)
