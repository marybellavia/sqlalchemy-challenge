import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h2>Available Routes:</h2>"
        f"<ul> <li><a href=http://127.0.0.1:5000/api/v1.0/precipitation>/api/v1.0/precipitation</a></li>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations>/api/v1.0/stations</a></li>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs>/api/v1.0/tobs</a></li>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/<start>/api/v1.0/<start></a></li>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/<start>/<end>/api/v1.0/<start>/<end></a></li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """This query returns the last 12 months of precipitation data"""
    # gettign the precipitation data from the the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    # closing the session
    session.close()

    # Converting list of tuples into a dictionary
    prcp_dict = {}
    for date, prcp in results:
        if prcp_dict[date]:
            prcp_dict[date] += prcp
        else:
            prcp_dict[date] = prcp

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Returning a list of all the stations"""
    # getting all the stations
    results = session.query(Station.station).all()

    # closing session
    session.close()
    
    # converting results into a list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    """Returning a list of the stats for the most active station"""
    # finding the most active station
    sel = [Measurement.station, func.count(Measurement.prcp)]
    station_counts = session.query(*sel).group_by(Measurement.station).order_by(sel[1]).all()
    most_active = station_counts[-1][0]

    # doing calculations for most active
    sel = [Measurement.station, 
       func.min(Measurement.tobs), 
       func.max(Measurement.tobs), 
       func.avg(Measurement.tobs)]
    results = session.query(*sel).filter(Measurement.station == most_active).all()

    # closing session
    session.close()

    # converting results into a list to jsonify
    most_active_stats = list(np.ravel(results))

    return jsonify(most_active_stats)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start = None, end = None):
    session = Session(engine)
    if end != None:
        sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        results = session.query(*sel).filter((Measurement.date >= start) and (Measurement.date <= end)).all()

        start_end_date = list(np.ravel(results))
        # closing session
        session.close()
        return jsonify(start_end_date)
    else:
        sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
        results = session.query(*sel).filter(Measurement.date >= start).all()

        start_date = list(np.ravel(results))

        # closing session
        session.close()
        return jsonify(start_date)


if __name__ == '__main__':
    app.run(debug=True)
