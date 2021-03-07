import sqlite3
from flask import Flask, jsonify
from http import HTTPStatus

DATABASE = 'db.sqlite3'

TYPES = [
        "dailycases",
        "dailyrecovered",
        "dailydeaths",
        "activecases",
        "activecasesper100k",
        "dailycasessmooth",
        "dailyrecoveredsmooth",
        "dailydeathssmooth",
        "mortality",
        "casefatality",
        "incidencerate",
    ]

app = Flask(__name__)


@app.route('/api')
def get_example():
    return jsonify({'example': '/api/[data_types]/[country_iso2]/<date_top>/<date_end>', 'data_types': TYPES}),\
           HTTPStatus.OK


@app.route('/api/<string:typ>')
@app.route('/api/<string:typ>/<string:iso2>')
@app.route('/api/<string:typ>/<string:iso2>/<string:date_top>')
@app.route('/api/<string:typ>/<string:iso2>/<string:date_top>/<string:date_end>')
def get_covid(typ, iso2=None, date_top=None, date_end=None):
    message = "message"
    if typ not in TYPES:
        return jsonify({message: f"Typ '{typ}' not found"}), HTTPStatus.NOT_FOUND
    if iso2 is None:
        return jsonify({message: "Bad request"}), HTTPStatus.BAD_REQUEST
    if len(iso2) != 2:
        return jsonify({message: f"Iso2 '{iso2}' is bad"}), HTTPStatus.BAD_REQUEST
    country = db_country(iso2)
    if len(country) == 0:
        return jsonify({message: f"Country '{iso2}' not found"}), HTTPStatus.NOT_FOUND
    if date_top is not None and len(date_top) != 10:
        return jsonify({message: f"Date top '{date_top}' is bad"}), HTTPStatus.BAD_REQUEST
    if date_end is not None and len(date_end) != 10:
        return jsonify({message: f"Date end '{date_end}' is bad"}), HTTPStatus.BAD_REQUEST
    value = db_covid(typ, iso2, date_top, date_end)
    if len(value) == 0:
        return jsonify({message: f"Data types '{typ}' and iso2 '{iso2}' not found"}), HTTPStatus.NOT_FOUND
    return jsonify({f"{typ} {iso2.upper()} ({country})": value}), HTTPStatus.OK


def db_country(iso2):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    try:
        value = ""
        cur.execute(f"SELECT country FROM covid19_country WHERE iso2 = '{iso2.upper()}'")
        value = cur.fetchone()[0]
    except:
        value = ""
    con.close()
    return value


def db_covid(typ, iso2, date_top=None, date_end=None):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    sql = f"SELECT a.date,a.{typ} FROM covid19_covidcalc a LEFT JOIN covid19_country b ON b.id = a.country_id " \
          f"WHERE b.iso2 = '{iso2.upper()}' "
    if date_top is None:
        sql += f"and a.{typ} <> 0 "
    else:
        sql += f"and date >= '{date_top}' "
    if date_end is not None:
        sql += f"and date <= '{date_end}' "
    sql += "ORDER BY date"
    try:
        value = []
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            value.append(row)
    except:
        value = []
    con.close()
    return value


if __name__ == '__main__':
    app.run(debug=True)
