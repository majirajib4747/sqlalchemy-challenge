# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template, redirect #flask is a server


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

## Home Page
## It will display all the routes
@app.route("/")
def home():
        routes = ['http://127.0.0.1:5000/api/v1.0/precipitation',
                'http://127.0.0.1:5000/api/v1.0/stations',
                'http://127.0.0.1:5000/api/v1.0/tobs',
                'http://127.0.0.1:5000/api/v1.0/<start>',
                'http://127.0.0.1:5000/api/v1.0/<start>/<end>'
        ]
        return (routes)
## Precipitation Route 
## It will return 1 Year precipitation from 2016-08-23 to 2017-08-23 
@app.route('/api/v1.0/precipitation')
def precipitation():
#Return precipitation for last 1 Year ( 2016-08-23 - 2017-08-23) 
# Calculate the date one year from the last date in data set.
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
        results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_year).all()
        precipitation = list(np.ravel(results))
        return jsonify(precipitation)

## This route will query station table and return all the station ID and name 
@app.route('/api/v1.0/stations')
def stations():
## Return all Stattion Details
    station_results = session.query(station.station, station.name).all()   
    station_detail = list(np.ravel(station_results))
    return jsonify(station_detail)   

## This Route will display last year's temp for most active base : USC00519281
@app.route('/api/v1.0/tobs')
def temp():
## Return last years Temperature details for Station USC00519281
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_results = session.query(measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= prev_year).all()
    temp_detail_USC00519281 = list(np.ravel(temp_results))
    return jsonify(temp_detail_USC00519281)  

## This Route will display min,max and average temp for most active base : USC00519281 starting from start date through end date passed in the url
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')

def tempstart(start=None,end=None):
    if not end:
        temp_start_results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').filter(measurement.date >= start).all()
        temp_detail_start = list(np.ravel(temp_start_results))
        return jsonify(temp_detail_start)
    else :
        temp_start_end_results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').filter(measurement.date >= start).filter(measurement.date <= end).all()
        temp_detail_start_end = list(np.ravel(temp_start_end_results))
        return jsonify(temp_detail_start_end) 

if __name__ == '__main__':
    app.run(debug=True)

#################################################
# Flask Routes
#################################################
