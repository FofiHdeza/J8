import os
import urllib
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_pymongo import PyMongo
#from nornir import InitNornir
# from nornir.plugins.tasks.networking import napalm_get, netmiko_send_command, netmiko_send_config, tcp_ping
# from nornir.core.filter import F
# from netmiko import NetMikoTimeoutException
# import yaml
# import pymongo
# import pyodbc
# import jinja2
# import copy
# #import time
# import pyodbc
# import os

app = Flask(__name__)
#app_context = app.app_context()
#app_context.push()
app.config['SECRET_KEY'] = '52e65cabc8bd687dcce952f1390a61d2'
# #app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///proyecto.db'
# params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=base_de_datos_proyecto;UID=SA;PWD=Beforeforget123')
# #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://DESKTOP-VQ58E7S/base_de_datos_proyecto?driver=ODBC Driver 17 for SQL Server"
# #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://FOFILAPTOP/base_de_datos_proyecto?driver=ODBC Driver 17 for SQL Server"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
# #app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://192.168.3.100/base_de_datos_proyecto?driver=ODBC Driver 17 for SQL Server"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/Proyecto_equipos_de_red"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SERVER_NAME']='127.0.0.1:5000'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
# mongo = PyMongo(app)
login_manger= LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'
#nr = InitNornir(config_file="Web/config.yaml")
#app_context = app.app_context()
#app_context.push()
#nr = InitNornir(config_file="config.yaml")
#conn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=FOFILAPTOP;PORT=1433;DATABASE=base_de_datos_proyecto;Trusted_Connection=yes;')
#conn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=base_de_datos_proyecto;UID=SA;PWD=Beforeforget123;')
#conn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-VQ58E7S;PORT=1433;DATABASE=base_de_datos_proyecto;Trusted_Connection=yes;')
#c= conn.cursor()
#os.environ["NET_TEXTFSM"]= "/home/ubuntu/.local/lib/python3.6/site-packages/ntc_templates"
#os.environ["NET_TEXTFSM"]= "C:/Users/ivand/AppData/Local/Programs/Python/Python36/Lib/site-packages/ntc_templates"
#myclient = pymongo.MongoClient("mongodb://localhost:27017/Proyecto_equipos_de_red")
#mydb = myclient["Proyecto_equipos_de_red"]

#Rcol = mongo.db.Routers
#Scol =mongo.db.Switches
#Vcol = mongo.db.Vcircuit
#Pcol = mongo.db.Ippool

from Web import routes

