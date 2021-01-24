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
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/<start>/<end>>/api/v1.0/<start>/<end></a></li></ul>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """This query returns the last 12 months of precipitation data"""
    twelve_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into a dictionary
    prcp_dict = dict(np.ravel(twelve_months))

    return jsonify(prcp_dict)


# @app.route("/api/v1.0/stations")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)

# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     return null

if __name__ == '__main__':
    app.run(debug=True)
