#################################################
# Database Setup
#################################################

import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta

# initialize engine
database_path = "C:/Users/palan/NW-Data-Science/sqlalchemy-challenge/Data/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")
db_connection = engine.connect()

# declare a base using `automap_base()`
base = automap_base()

# use the base class to reflect the database tables
base.prepare(engine, reflect=True)

# map classes to base
Measurement = base.classes.measurement
Stations = base.classes.station


#################################################
# Flask Set Up
#################################################


# import Flask
from flask import Flask

# create an app, being sure to pass __name__
app = Flask('myApp')

# define what to do when a user hits the index route
@app.route("/")
def rootUrl():

    return """
        <div style="text-align:left;padding:50px;">
        
        <b>Available Routes:</b><br><br>
        /api/v1.0/precipitation/<br>
        /api/v1.0/stations/<br>
        /api/v1.0/tobs/<br>
        /api/v1.0/&lt;start_date&gt/&lt;end_date&gt

        </div>
        """

#################################################
# Precpitation Query
#################################################

@app.route("/api/v1.0/precipitation/<search_date>")
def precipitation(search_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data as json"""

    results = session.query(Measurement.date, Measurement.id, Measurement.station, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, id, station, prcp in results:

        if date == search_date:
            prcp_dict = {}
            prcp_dict["id"] = id
            prcp_dict["station"] = station
            prcp_dict["prcp"] = prcp
            all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

#################################################
# Station
#################################################

@app.route("/api/v1.0/stations")
def station():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return station data as json"""

    results = session.query(Stations.id, Stations.station, Stations.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for id, station, name in results:

            station_dict = {}
            station_dict["id"] = id
            station_dict["station"] = station
            station_dict["name"] = name
            all_stations.append(station_dict)

    return jsonify(all_stations)

#################################################
# TOBS
#################################################

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return station data as json"""

    query = "SELECT id, station, date, tobs FROM measurement WHERE station = 'USC00519281' AND date > '2016-08-10';"
    results = engine.execute(query).fetchall()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []
    for id, station, date, tobs in results:

            tobs_dict = {}
            tobs_dict["id"] = id
            tobs_dict["station"] = station
            tobs_dict["date"] = date
            tobs_dict["tobs"] = tobs
            all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

#################################################
# Temperature Stats
#################################################

@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_stats(start_date, end_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature data as json"""

    # Minimum temperature data
    min_temp_query = f"SELECT MIN(tobs) FROM measurement WHERE date BETWEEN '{start_date}' AND '{end_date}';"
    min_temp_result = engine.execute(min_temp_query).fetchall()

    # Maximum temperature data
    max_temp_query = f"SELECT MAX(tobs) FROM measurement WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    max_temp_result = engine.execute(max_temp_query).fetchall()

    # Average temperature data
    avg_temp_query = f"SELECT AVG(tobs) FROM measurement WHERE date BETWEEN '{start_date}' AND '{end_date}'"
    avg_temp_result = engine.execute(avg_temp_query).fetchall()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_tobs = []

    tobs_dict = {}

    tobs_dict["TMIN"] = min_temp_result[0][0]
    tobs_dict["TMAX"] = max_temp_result[0][0]
    tobs_dict["TAVG"] = round(avg_temp_result[0][0],0)
    all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

app.run()