from sqlalchemy import create_engine
from flask import Flask,jsonify,render_template
import pandas as pd
from sqlalchemy.ext.automap import automap_base
import ast
import matplotlib.path as mplPath
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json
import urllib
from apscheduler.schedulers.background import BackgroundScheduler

engine = create_engine('postgresql://postgres:testpassword@unidades-db.cuzb9dl0k6mc.us-east-2.rds.amazonaws.com:5432/postgres')
#Engine url with password included


#Functions used to update the database
def loc_alcaldias_json(x):#This function finds if a point is inside a polygon
    lat=x["position_latitude"]
    lon=x["position_longitude"]

    querystring=f"select * from alcaldias "
    alcaldias=engine.execute(querystring)
    alcdata=[]
    for element in alcaldias:
        getdict={}
        getdict['id']= element.id
        getdict['alcaldia']= element.alcaldia
        getdict['geo_shape']= element.geo_shape
        alcdata.append(getdict) 
    for x in alcdata:
        
        polygon=ast.literal_eval(x["geo_shape"])#converts text into code, in this case a list of lists
        poly_path = mplPath.Path(np.array(polygon))#creates the polygon from the data
        point = (lon, lat)
        inalc=poly_path.contains_point(point)#finds if 
        if inalc:
            return x["alcaldia"]

def update_db():
    print("Updating database...")
    limit=2 #designates the maximum amount of updated data that is read from the data source
    #Gets data from the data source
    url = f'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ad360a0e-b42f-482c-af12-1fd72140032e&limit={limit}'  
    fileobj = urllib.request.urlopen(url)
    newdata=json.load(fileobj)
    records=newdata['result']['records']#selects only the rults from the data and not the other sources
    querystring="select max(id) as id from viajes"
    getmaxid=engine.execute(querystring)
    for x in getmaxid:
        print(x[0])
        idnum=x[0]+1
        print(idnum)
    session=Session(engine)
    for x in records:#creates a class with the same attributes as the one in the database and inserts data from the data source
        uploadclass=viajes() 
        uploadclass.id=idnum
        uploadclass.vehicle_id=x["vehicle_id"]
        uploadclass.vehicle_current_status=x["vehicle_current_status"]
        uploadclass.position_longitude=x["position_longitude"]
        uploadclass.position_speed=x["position_speed"]
        uploadclass.trip_schedule_relationship=x["trip_schedule_relationship"]
        uploadclass.vehicle_label=x["vehicle_label"]
        uploadclass.date_updated=x["date_updated"]
        uploadclass.position_latitude=x["position_latitude"]
        uploadclass.geographic_point=x["geographic_point"]
        uploadclass.position_odometer=x["position_odometer"]
        uploadclass.alcaldia=loc_alcaldias_json(x)
        #Note: trip_id and trip_start_date are not included in the database as they sometimes are null.
        idnum=idnum+1
        session.add(uploadclass)
    session.commit()
    session.close()



# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)
viajes=Base.classes.viajes #viajes is used for purposes of database updating

#updating the database in a fixed schedule
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_db, trigger="interval", minutes=20)
scheduler.start()#will update the database every 20 minutes with new data





app = Flask(__name__)
@app.route("/")
def index():
    return "Available commands   /availunits   /unitdata/[unitid]      /listaalcaldias       /unitsinalcaldia/[alcaldia]"


@app.route("/availunits")
def availunits():
    querystring="select distinct vehicle_id from viajes" #query to get all the distinct vehicle IDs from the database
    data=engine.execute(querystring)#executes the query
    jsondata=[]
    for element in data: #this loop adds data to a dictionary, which then appends it to a list, which is then returned as a json
        getdict={}
        getdict['vehicle_id']= element.vehicle_id
        jsondata.append(getdict) 

    return jsonify(jsondata)

@app.route("/unitdata/<unitid>")
def unitdata(unitid):
    querystring=f"""select position_latitude,position_longitude,date_updated from viajes
                    where vehicle_id={unitid}"""  #query to get data from a particular unit from the database
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:#this loop adds data to a dictionary, which then appends it to a list, which is then returned as a json
        getdict={}
        getdict['position_latitude']= element.position_latitude
        getdict['position_longitude']= element.position_longitude
        getdict['date_updated']= element.date_updated
        getdict['alcaldia']= element.date_updated
        jsondata.append(getdict) 

    return jsonify(jsondata)

@app.route("/listaalcaldias")
def alcaldias():
    querystring=f"select alcaldia from alcaldias" #query the list of alcaldias from the database
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:#this loop adds data to a dictionary, which then appends it to a list, which is then returned as a json
        getdict={}
        getdict['alcaldia']= element.alcaldia
        jsondata.append(getdict) 
    return jsonify(jsondata)

@app.route("/unitsinalcaldia/<alcaldia>")
def unitsinalcaldia(alcaldia):
    querystring=f"""select vehicle_id from viajes
                    where (alcaldia='{alcaldia}')"""  #query to get the units in an alcaldia from the database   
    data=engine.execute(querystring)
    jsondata=[]
    for element in data:#this loop adds data to a dictionary, which then appends it to a list, which is then returned as a json
        getdict={}
        getdict['vehicle_id']= element.vehicle_id
        jsondata.append(getdict) 
    return jsonify(jsondata)


if __name__ == "__main__":
    app.run(debug=True)
#testing to update again