#importing dependencies and chicago.py to use getData function
import chicago
import sqlite3
import json
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect

app = Flask(__name__)

#################################################
# Database Setup
#################################################
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chicago_data.db'

engine = create_engine("sqlite:///chicago_data.db")
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect thes
Base.prepare(db.engine, reflect=True)

# Create the inspector and connect it to the engine
inspector = inspect(engine)

# Collect the names of tables within the database
tables = inspector.get_table_names()
for x in tables:
    print(x["name"])

# Save references to each table
# Doesn't work w / out primary keys!
potato = Base.classes.chicago_data
aggs_overall = Base.classes.aggs_overall
aggs_by_date_type = Base.classes.aggs_by_date_type
dfCSV = Base.classes.dfCSV
group_type_df = Base.classes.group_type_df
month_day = Base.classes.month_day

#home route to hold initial visuals which need to be updated with button press
@app.route("/")
def home():
    print("chicago_data table: ", potato.query.count())
    print("aggs_overall table: ", aggs_overall.query.count())
    print("aggs_by_date_type table: ", aggs_by_date_type.query.count())
    print("dfCSV table: ", dfCSV.query.count())
    print("group_type_df table: ", group_type_df.query.count())
    print("Total number of rows in groupby_df table: ", month_day.query.count())

    return render_template("index.html")

@app.route("/updateData")
def getData():

    # Run the data function with error handling for failed data loading
    try:
        chicago.getData()
        print('Updated data loaded successfully')
        return render_template("index.html")

    except:
        print("Data updating failed")

@app.route("/table_data")
def table_data():
    # Use Pandas to perform the sql query
    stmt = db.session.query(aggs_by_date_type).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

if __name__ == '__main__':
    app.run(debug=True)