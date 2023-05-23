# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime
from datetime import timedelta
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement

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
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Set a time variable
    time_year=datetime.date (2017, 8, 23) - timedelta(days=365)
    #Query prcp based on recent date
    results = session.query(Measurement.prcp,Measurement.date).filter(Measurement.date >= time_year).all()
    #list out result
    year_precipitation = list(np.ravel(results)) 
    #Close session
    session.close()   
    
    return jsonify(year_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query all stations
    results=session.query(Measurement.station).all()
    #Close session
    session.close()
    #list out result
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session link
    session = Session(engine)
    #Set a time variable
    time_year=datetime.date (2017, 8, 23) - timedelta(days=365)
    most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281')\
    .filter(Measurement.date >= time_year).all()
    #list out result
    show_active_station= list(np.ravel(most_active_station))

    #Close session
    session.close()
    
    return jsonify(show_active_station)
   
    
@app.route("/api/v1.0/<start_date>")
@app.route("/api/v1.0/<start_date>/<end_date>")
def start(start_date=None, end_date=None):
    
    #Create session link
    session = Session(engine)
    
    #If not end_date is start_date
    if not end_date:
        #accept start_date in format
        start_date = datetime.datetime.strptime(start_date,'%m%d%Y')
        #Query session and calc min, max, avg
        results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
        #Close connection
        session.close()
        #list out results
        st_date= list(np.ravel(results)) 
        
        return jsonify(st_date)
    
    #else start date and end date
    start_date = datetime.datetime.strptime(start_date,'%m%d%Y')
    #accept end_date in format
    end_date = datetime.datetime.strptime(end_date,'%m%d%Y')
    #Query session and calc min, max, avg
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    #Close connection
    session.close()
    #list out results
    date= list(np.ravel(results)) 
        
    return jsonify(date)
    
if __name__ == '__main__':
    app.run(debug=True)