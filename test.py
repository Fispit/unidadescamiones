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
engine = create_engine('postgresql://postgres:testpassword@unidades-db.cuzb9dl0k6mc.us-east-2.rds.amazonaws.com:5432/postgres')
