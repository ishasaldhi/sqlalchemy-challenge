# Import the dependencies.
import sqlAlchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_wit  = engine)

# Save references to each table
Measurements = Base.classes.measurements
Stations = Base.classes.measurements

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


twelve_months = '2016-08-23'
active_station_id = "USC00519281"
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
            )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results =  session.query(Measurements.date, func.avg(Measurements.prcp)).\
        filter(Measurements.date >= twelve_months).\
        group_by(Measurements.date).all()

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Stations.station, Stations.name).all()

    jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    tresults = session.query(Measurements.date, Measurements.station, Measurements.tobs).\
        filter(Measurements.station == active_station_id).\
        filter(Measurements.date >= twelve_months)
    
    return(tresults)

@app.route("/api/v1.0/<start>")
def start(date):
    daytemp = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= date).all
    return jsonify(daytemp)
    
@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    temps = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all

    return jsonify(temps)
    