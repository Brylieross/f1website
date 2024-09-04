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


# Home page
@app.route('/')
def homepage():
    return render_template("home.html")


# Drivers data page
@app.route("/drivers")
def drivers():
    cursor = get_db().cursor()
    sql = """SELECT Driver.driver_id, Driver.name, Driver.driver_number, Driver.championships, Driver.country, Driver.time_period, Teams.name, Driver.race_wins
            FROM Driver
            JOIN Teams ON Driver.last_team = Teams.team_id"""
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("drivers.html", results=results)


# Teams data page
@app.route("/teams")
def teams():
    cursor = get_db().cursor()
    sql = "SELECT * FROM Teams"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("teams.html", results=results)


# Different years with who was 1st 2nd and 3rd data page
@app.route("/year")
def year():
    cursor = get_db().cursor()
    sql = "SELECT year_id FROM Year" 
    cursor.execute(sql)
    yearnum = len(cursor.fetchall())
    fulldata = []
    for j in range(yearnum):
        i = j+1
        cursor.execute("SELECT year, first, second, third FROM Year WHERE year_id = ?", (i,))
        tempdata = cursor.fetchall()
        cursor.execute("SELECT name FROM Driver WHERE driver_id = ?", (tempdata[0][1],))
        d1 = cursor.fetchone()
        cursor.execute("SELECT name FROM Driver WHERE driver_id = ?", (tempdata[0][2],))
        d2 = cursor.fetchone()
        cursor.execute("SELECT name FROM Driver WHERE driver_id = ?", (tempdata[0][3],))
        d3 = cursor.fetchone()
        fulldata.append([tempdata[0][0],d1[0],d2[0],d3[0]])
    return render_template("year.html", results=fulldata)


# Search for drivers
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    results = []
    if query:
        cursor = get_db().cursor()
        sql = """SELECT Driver.driver_id, Driver.name, Driver.driver_number, Driver.championships, Driver.country, Driver.time_period, Teams.name, Driver.race_wins
                FROM Driver
                JOIN Teams ON Driver.last_team = Teams.team_id
                WHERE Driver.name LIKE ?"""
        cursor.execute(sql, ('%' + query + '%',))
        results = cursor.fetchall()
    return render_template("search.html", results=results)


# Error 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)