import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
mm = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/rain<br/>"
        # f"/api/v1.0/stations<br/>"
        # f"/api/v1.0/tobs<br/>"
    )

@app.route("/api/v1.0/rain")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(mm.date, mm.station, mm.prcp, mm.tobs).order_by(mm.date).all()

    session.close()

    # Convert list of tuples into normal list
    # all_rain = list(np.ravel(results))

    #Sort values in tuples into relevant lists. 
   
    all_rain = []
    for date, station, prcp, tobs in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["station_name"] = station
        rain_dict["prcp"] = prcp
        rain_dict["tobs"] = tobs
        all_rain.append(rain_dict)

    return jsonify(all_rain)


if __name__ == '__main__':
    app.run(debug=True)