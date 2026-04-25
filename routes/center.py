from flask import  Flask , jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
import database

center = Blueprint("center", __name__)

@center.route("/")
def get_center():
    conn = database.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
                select * from center
            """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)
    

@center.route("/", methods=["POST"])
def create_center():
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                insert into center
                    (city, driver_id)
                values (%s, %s, %s)
            """, ( data["weight"],  data["driver_id"] ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Created"}), 201

@center.route("/<string:id>", methods=["DELETE"])
def delete_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute("""
                delete from center where center_id = %s
            """, ( id, ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Deleted"}), 201


@center.route("/<string:id>", methods=["PUT"])
def update_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                
                update center 
                set city = %s
                    driver_id = %s
                where center_id = %s 

            """, ( data["city"],  data["driver_id"], id ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Updated"}), 201