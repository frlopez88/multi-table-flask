from flask import  Flask , jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
import database

vehicle = Blueprint("vehicle", __name__)

@vehicle.route("/")
def get_vehicle():
    conn = database.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
                select * from vehicle
            """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)
    

@vehicle.route("/vehicle", methods=["POST"])
def create_vehicle():
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                insert into vehicle
                    (license_plate, model, capacity, driver_id)
                values (%s, %s, %s,%s)
            """, ( data["license_plate"], data["model"], data["capacity"], data["driver_id"] ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Created"}), 201

@vehicle.route("/<string:id>", methods=["DELETE"])
def delete_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute("""
                delete from vehicle where license_plate = %s
            """, ( id, ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Deleted"}), 201


@vehicle.route("/<string:id>", methods=["PUT"])
def update_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                
                update vehicle 
                set model = %s, 
                    capacity = %s, 
                    driver_id = %s
                where license_plate = %s 

            """, ( data["model"],data["capacity"],  data["driver_id"], id ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Updated"}), 201