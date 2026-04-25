from flask import Flask , jsonify, request
from psycopg2.extras import RealDictCursor
from database import init_db

#import routes
from routes.vehicle import vehicle
from routes.driver import driver

app = Flask(__name__)

## this will create the tables if not exists
init_db()

app.register_blueprint(vehicle, url_prefix= "/vehicle")
app.register_blueprint(driver, url_prefix= "/driver")

@app.route("/")
def home():
    return jsonify( {"message": "server online"} ) , 200


if __name__ == "__main__":
    app.run(debug=True)