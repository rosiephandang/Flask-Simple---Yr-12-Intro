import sqlite3
from flask import Flask, g # render_template

DATABASE = 'database.db'

#initialise app
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

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close() 
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    # home page - return just the model name, image URL manufacturer and fuselage for all commercial airrcraft in the database
    sql = """SELECT Commercial_aircraft.model_name,
      Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name
        FROM Commercial_aircraft
        INNER JOIN Manufacturer
        ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id 
        INNER JOIN Fuselage
        ON Commercial_aircraft.fuselage_id = Fuselage.type_id
        ORDER BY Commercial_aircraft.model_name ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string

@app.route('/aircraft/<int:model_id>')
def aircraft(model_id):
    # return all details for a specific model of commercial aircraft
    sql = """SELECT Commercial_aircraft.model_name,  Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name, Commercial_aircraft.top_speed_kmph, Commercial_aircraft.max_people_capacity, Commercial_aircraft.max_distance_km, Commercial_aircraft.max_takeoff_weight_kg,Commercial_aircraft.fuel_capacity_L
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
WHERE Commercial_aircraft.aircraft_id = ?;"""
    result = query_db(sql, (model_id,), one=True)
    return str(result) # for testing purposes, we will just return the result as a string

if __name__ == "__main__":
    app.run(debug=True)