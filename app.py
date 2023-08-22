# Import the dependencies.
import numpy as np
import datetime as dt
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
Base.prepare(autoload_with = engine)
# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save references to each table


# Create our session (link) from Python to the DB
# session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
recent_date = dt.date(2017,8,23)
f_date = recent_date - dt.timedelta(days = 365)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)



    plot_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= f_date).filter(Measurement.date <=recent_date).all()

    session.close()
    all_prcp = []
    for date, prcp in plot_data:
        passenger_dict = {}
        passenger_dict["date"] = date
        passenger_dict["prcp"] = prcp
        all_prcp.append(passenger_dict)
 

    return jsonify(all_prcp)





@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station = session.query(Measurement.station).group_by(Measurement.station).all()



    session.close()
    all_stations = list(np.ravel(station))

 
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def active_station():

    session = Session(engine)

    ac_station = session.query( Measurement.tobs, Measurement.date).filter(Measurement.date >= f_date).filter(Measurement.date <=recent_date).filter(Measurement.station == 'USC00519281').all()



    session.close()
    all_ac_stations = list(np.ravel(ac_station))

 
    return jsonify(all_ac_stations)




@app.route("/api/v1.0/<start>")
def start_date(start):



    session = Session(engine)

    summary = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()



    session.close()
    all_summary = list(np.ravel(summary))

 
    return jsonify(all_summary)










if __name__ == '__main__':
    app.run(debug=True)
