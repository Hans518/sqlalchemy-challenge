import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from scipy import stats


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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )

@app.route("/api/v1.0/rain")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all rain data 
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

@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query Station data
    stations = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()

    all_stations = []
    for id, station, name, latitude, longitude, elevation in stations:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations_dict["latitude"] = latitude
        stations_dict["longitude"] = longitude
        stations_dict["elevation"] = elevation
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query observed temp data
    temp_data = session.query(mm.station, mm.date, mm.tobs).filter(mm.station == 'USC00519281').filter(mm.date >= '2016-08-18' ).order_by(mm.date).all()

    session.close()

    all_temps = []
    for station, date, tobs in temp_data:
        temp_dict = {}
        temp_dict["station"] = station
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    temp_calc = session.query(func.min(mm.tobs), func.max(mm.tobs), func.avg(mm.tobs)).\
        filter(mm.date >= start).all()

    session.close()

    temp_end = []
    for temp_min, temp_max, temp_avg in temp_calc:
        temp_dict = {}
        temp_dict["Min temp"] = temp_min
        temp_dict["Max temp"] = temp_max
        temp_dict["Agv temp"] = temp_avg
        temp_end.append(temp_dict)

    
    return jsonify(temp_end)

@app.route("/api/v1.0/<start>/<end>")
def calc_date_range(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start (string): A date string in the format %Y-%m-%d
        end (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    # Create our session (link) from Python to the DB
    session = Session(engine)

    date_range = session.query(func.min(mm.tobs), func.max(mm.tobs), func.avg(mm.tobs)).\
        filter(mm.date >= start).filter(mm.date <= end).all()

    session.close()

    temp_start_end = []
    for temp_min, temp_max, temp_avg in date_range:
        temp_dict = {}
        temp_dict["Min temp"] = temp_min
        temp_dict["Max temp"] = temp_max
        temp_dict["Agv temp"] = temp_avg
        temp_start_end.append(temp_dict)

    return jsonify(temp_start_end)


if __name__ == '__main__':
    app.run(debug=True)