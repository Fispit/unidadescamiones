import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify,render_template
import datetime
import pandas as pd
from flask_cors import CORS
import ast

engine = create_engine(f'postgresql://postgres:testpassword@unidades-db.cuzb9dl0k6mc.us-east-2.rds.amazonaws.com:5432/postgres')
reduction_ratio=100
routesnum=250
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stationdata")
def stationdata():
    querystring="select * from Estaciones"
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:
        getdict={}
        getdict['ID']= element.e_id
        getdict['Name']= element.name
        getdict['LAT']= element.lat
        getdict['Lon']= element.lon
        getdict['districtName']= element.districtname
        jsondata.append(getdict) 

    return jsonify(jsondata)




@app.route("/availunits")
def availunits():
    querystring="select distinct vehicle_id from viajes"
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:
        getdict={}
        getdict['vehicle_id']= element.vehicle_id
        jsondata.append(getdict) 

    return jsonify(jsondata)

@app.route("/unitdata/<unitid>")
def availunits(unitid):
    querystring=f"""select * from viajes
                    where vehicle_id={unitid}"""
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:
        getdict={}
        getdict['vehicle_id']= element.vehicle_id
        jsondata.append(getdict) 

    return jsonify(jsondata)
if __name__ == "__main__":
    app.run(debug=True)
#testing to update again