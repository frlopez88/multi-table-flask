from flask import  Flask , jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
import database

shipment = Blueprint("shipment", __name__)

@shipment.route("/")
def get_shipment():
    conn = database.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
                select * from shipment
            """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)
    

@shipment.route("/", methods=["POST"])
def create_shipment():
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                insert into shipment
                    (weight, destination, driver_id)
                values (%s, %s, %s)
            """, ( data["weight"], data["destination"], data["driver_id"] ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Created"}), 201

@shipment.route("/<string:id>", methods=["DELETE"])
def delete_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute("""
                delete from shipment where tracking_number = %s
            """, ( id, ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Deleted"}), 201


@shipment.route("/<string:id>", methods=["PUT"])
def update_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                
                update shipment 
                set weight = %s, 
                    destination = %s, 
                    driver_id = %s
                where tracking_number = %s 

            """, ( data["weight"],data["destination"],  data["driver_id"], id ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Updated"}), 201