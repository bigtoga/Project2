#importing dependencies and chicago.py to use getData function
import chicago
import sqlite3
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#setting route to chicago database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chicago_data.db'
db = SQLAlchemy(app)

#reflects the current database into the primary index.html
db.Model.metadata.reflect(db.engine)

#creates a model of the reflection, allowing for queries to be made (example: crime.query.count())
class crime(db.Model):
    __tablename__ = 'chicago_data'
    __table_args__ = { 'extend_existing': True }
    index = db.Column(db.Text, primary_key=True)

#home route to hold initial visuals which need to be updated with button press
@app.route("/")
def home():
    print("Total number of schools is", crime.query.count())
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

if __name__ == '__main__':
    app.run(debug=True)