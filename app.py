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

@app.route('/airbus')
def airbus():
    # airbus page - return just the model, manufacturer, fuselage sorted by manufacturer (Airbus)
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id 
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
WHERE manufacturer_name = 'Airbus'
ORDER BY Commercial_aircraft.model_name ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/boeing')
def boeing():
    # boeing page - return just the model, manufacturer, fuselage sorted by manufacturer (Boeing)
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id 
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
WHERE manufacturer_name = 'Boeing'
ORDER BY Commercial_aircraft.model_name ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/narrow')
def narrow():
    # narrow page - return just the model, manufacturer, fuselage sorted by fuselage (narrow)
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id 
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
WHERE Fuselage.type_name = 'Narrow-body'
ORDER BY Commercial_aircraft.model_name ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/wide')
def wide():
    # wide page - return just the model, manufacturer, fuselage sorted by fuselage (wide)
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id 
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
WHERE Fuselage.type_name = 'Wide-body'
ORDER BY Commercial_aircraft.model_name ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/people_capacity')
def people_capacity():
    # people capacity page - return just the model, manufacturer, fuselage sorted by people capacity
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name,Commercial_aircraft.max_people_capacity  
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
ORDER BY Commercial_aircraft.max_people_capacity ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/max_distance')
def max_distance():
    # max distance page - return just the model, manufacturer, fuselage sorted by max distance
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name,Commercial_aircraft.max_distance_km  
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
ORDER BY Commercial_aircraft.max_distance_km ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/top_speed')
def top_speed():
    # top speed page - return just the model, manufacturer, fuselage sorted by top speed
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name,Commercial_aircraft.top_speed_kmph  
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
ORDER BY Commercial_aircraft.top_speed_kmph ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/max_takeoff_weight')
def max_takeoff_weight():
    # max takeoff weight page - return just the model, manufacturer, fuselage sorted by max takeoff weight
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name,Commercial_aircraft.max_takeoff_weight_kg  
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
ORDER BY Commercial_aircraft.max_takeoff_weight_kg ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


@app.route('/fuel_capacity')
def fuel_capacity():
    # fuel capacity page - return just the model, manufacturer, fuselage sorted by fuel capacity
    sql = """SELECT Commercial_aircraft.model_name,Commercial_aircraft.image_url,Manufacturer.manufacturer_name, Fuselage.type_name,Commercial_aircraft.fuel_capacity_L 
FROM Commercial_aircraft
INNER JOIN Manufacturer
ON Commercial_aircraft.manufacture_id = Manufacturer.manufacturer_id
INNER JOIN Fuselage
ON Commercial_aircraft.fuselage_id = Fuselage.type_id
ORDER BY Commercial_aircraft.fuel_capacity_L ASC;"""
    results = query_db(sql)
    return str(results) # for testing purposes, we will just return the results as a string


if __name__ == "__main__":
    app.run(debug=True)