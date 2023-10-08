# Import the dependencies.
from flask import Flask, jsonify


import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=True)

Base = automap_base()

Base.prepare(engine, reflect=True)


# reflect an existing database into a new model

measurement = Base.classes.measurement
station = Base.classes.station


# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return(
        "Welcome to the available routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/{start}<br/>"
        "/api/v1.0/{start}/{end}<br/>"
    ) 

@app.route("/api/v1.0/precipitation")
def percipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# Query session 
    prcp_query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    session.close()

# Formats query 
    weather_df = pd.DataFrame(prcp_query, columns=["date", "prcp"])
    data = dict(zip(weather_df["date"],weather_df["prcp"]))


@app.route("/api/v1.0/stations")
def stations():
    ttl_stations = session.query(func.count(station.station)).all()
    session.close()


# Query session
    ttl_stations = session.query(func.count(station.station)).all()
    session.close()

# Format the query 
    data = zip(ttl_stations, ["station"])

@app.route("/api/v1.0/tobs")
def temperature():
    active_station = session.query(measurement.station, func.count(measurement.station))\
.group_by(measurement.station)\
.order_by(func.count(measurement.station).desc())\
.all()
# Query session
    station_temp = session.query(measurement.date, measurement.tobs).\
                             filter(measurement.date >= year_ago).filter(measurement.station == "USC00519281").all()
    session.close()

# Format the query
    observation_data_df = pd.DataFrame(station_temp, columns=["date", "tobs"])
    data = dict(zip(observation_data_df["date"],observation_data_df["tobs"]))

# Sends data to app
return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

