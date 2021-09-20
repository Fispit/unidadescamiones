from sqlalchemy import create_engine
from flask import Flask,jsonify,render_template
import pandas as pd
from flask_cors import CORS
import ast

engine = create_engine('postgresql://postgres:testpassword@unidades-db.cuzb9dl0k6mc.us-east-2.rds.amazonaws.com:5432/postgres')
# reflect an existing database into a new model
# reflect the tables
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    print("Base")



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
def unitdata(unitid):
    querystring=f"""select position_latitude,position_longitude,date_updated from viajes
                    where vehicle_id={unitid}"""
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:
        getdict={}
        getdict['position_latitude']= element.position_latitude
        getdict['position_longitude']= element.position_longitude
        getdict['date_updated']= element.date_updated
        getdict['alcaldia']= element.date_updated
        jsondata.append(getdict) 

    return jsonify(jsondata)

@app.route("/listaalcaldias")
def alcaldias():
    querystring=f"select alcaldia from alcaldias "
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:
        getdict={}
        getdict['alcaldia']= element.alcaldia
        jsondata.append(getdict) 
    return jsonify(jsondata)

@app.route("/unitsinalcaldia/<alcaldia>")
def unitsinalcaldia(alcaldia):
    querystring=f"""select vehicle_id from viajes
                    where (alcaldia='{alcaldia}')"""     
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