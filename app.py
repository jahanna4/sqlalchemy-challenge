from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)

Measurement = base.classes.measurement
Station = base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    """List all available routes"""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """query results"""
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    precip = []
    for date, prcp in results:
        precip_info = {}
        precip_info["Date"] = date
        precip_info["Precipitation"] = [prcp]
        precip.append(precip_info)
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations_list():
    """list of stations"""
    session = Session(engine)

    results = session.query(Station.station, Station.name).all()
    session.close()

    list_of_stations = []
    for station, name in results:
        station_info = {}
        station_info["Station"] = station
        station_info["Station Name"] = name
        list_of_stations.append(station_info)
    
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    """temperature observations"""
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').limit(12).all()
    session.close()

    temp_obs = []
    for station, date, tobs in results:
        observations = {}
        observations["Station"] = station
        observations["Date"] = date
        observations["Temperature Observations"] = tobs
        temp_obs.append(observations)
    
    return jsonify(temp_obs)

@app.route("/api/v1.0/2017-01-18")
def averages_for_start_dates():
    """min, max, average temperatures for specified dates"""
    session = Session(engine)

    start_date = '2017-01-18'
    resultmin = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    resultavg = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    resultmax = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()
    results = [resultmin, resultavg, resultmax]

    min_dates_obs = []
    max_dates_obs = []
    avg_dates_obs = []
    for resultavg in results:
        avgreadings = {}
        avgreadings["Avg Temp"] = resultavg
        avg_dates_obs.append(avgreadings)

    for resultmin in results:
        minreadings = {}
        minreadings["Min Temp"] = resultmin
        min_dates_obs.append(minreadings)
    
    for resultmax in results:
        maxreadings = {}
        maxreadings["Max Temp"] = resultmax
        max_dates_obs.append(maxreadings)

    return jsonify(avg_dates_obs, min_dates_obs, max_dates_obs)

@app.route("/api/v1.0/2017-01-18/2017-01-28")
def averages_for_start_and_end_dates():
    """min, max, average temperatures for specified dates"""
    session = Session(engine)

    start_date = '2017-01-18'
    end_date = '2017-01-28'
    resultmin = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    resultavg = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    resultmax = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    results = [resultmin, resultavg, resultmax]

    min_dates_obs = []
    max_dates_obs = []
    avg_dates_obs = []
    for resultavg in results:
        avgreadings = {}
        avgreadings["Avg Temp"] = resultavg
        avg_dates_obs.append(avgreadings)

    for resultmin in results:
        minreadings = {}
        minreadings["Min Temp"] = resultmin
        min_dates_obs.append(minreadings)
    
    for resultmax in results:
        maxreadings = {}
        maxreadings["Max Temp"] = resultmax
        max_dates_obs.append(maxreadings)

    return jsonify(avg_dates_obs, min_dates_obs, max_dates_obs)



if __name__ == "__main__":
    app.run(debug=True)
    