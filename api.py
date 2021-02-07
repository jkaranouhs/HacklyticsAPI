import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Current COVID-19 Archive</h1>
<p>A prototype API for data regarding Coronavirus around the world.</p>'''


@app.route('/api/data/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('data.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_data = cur.execute('SELECT * FROM data;').fetchall()

    return jsonify(all_data)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/data', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('SNo')
    observation_date = query_parameters.get('ObservationDate')
    province_state = query_parameters.get('ProvinceState')
    country_region = query_parameters.get('CountryRegion')
    last_update = query_parameters.get('Last_Update')
    confirmed = query_parameters.get('Confirmed')
    deaths = query_parameters.get('Deaths')
    recovered = query_parameters.get('Recovered')

    query = "SELECT * FROM data WHERE"
    to_filter = []

    if id:
        query += ' SNo=? AND'
        to_filter.append(id)
    if observation_date:
        query += ' ObservationDate=? AND'
        to_filter.append(observation_date)
    if province_state:
        query += ' ProvinceState=? AND'
        to_filter.append(province_state)
    if country_region:
        query += ' CountryRegion=? AND'
        to_filter.append(country_region)
    if last_update:
        query += ' Last_Update=? AND'
        to_filter.append(last_update)
    if confirmed:
        query += ' Confirmed=? AND'
        to_filter.append(confirmed)
    if deaths:
        query += ' Deaths=? AND'
        to_filter.append(deaths)
    if recovered:
        query += ' Recovered=? AND'
        to_filter.append(recovered)
    if not (id or observation_date or province_state or country_region or last_update or confirmed or deaths or recovered):
        return page_not_found(404)

    query = query[:-9] + ';'

    conn = sqlite3.connect('data.sqlite')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
