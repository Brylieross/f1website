from flask import Flask, render_template, g, request
import sqlite3


DATABASE = 'F1.db'
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Home page
@app.route('/')
def homepage():
    return render_template("home.html")


#Drivers data page
@app.route("/drivers")
def drivers():
    cursor = get_db().cursor()
    sql = "SELECT * FROM Driver"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("drivers.html", results=results)


#Teams data page
@app.route("/teams")
def teams():
    cursor = get_db().cursor()
    sql = "SELECT * FROM Teams"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("teams.html", results=results)


#Different years data page
@app.route("/year")
def year():
    cursor = get_db().cursor()
    sql = "SELECT * FROM Year"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("year.html", results=results)


#Search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = []
    if query:
        cursor = get_db().cursor()
        sql = "SELECT * FROM Driver WHERE name LIKE ?"
        cursor.execute(sql, ('%' + query + '%',))
        results = cursor.fetchall()
    return render_template("search.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)