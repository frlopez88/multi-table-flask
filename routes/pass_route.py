from flask import  Flask , jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
import database

pass_bp = Blueprint("pass_bp", __name__)

@pass_bp.route("/")
def get_pass_bp():
    conn = database.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
                select * from pass
            """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)
    

@pass_bp.route("/", methods=["POST"])
def create_pass_bp():
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                insert into pass
                    (tracking_number, center_id, date)
                values (%s, %s, %s)
            """, ( data["tracking_number"], data["center_id"], data["date"] ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Created"}), 201

@pass_bp.route("/<string:id>", methods=["DELETE"])
def delete_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute("""
                delete from pass where pass_id = %s
            """, ( id, ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Deleted"}), 201


@pass_bp.route("/<string:id>", methods=["PUT"])
def update_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                
                update pass 
                set tracking_number = %s, 
                    center_id = %s, 
                    date = %s
                where pass_id = %s 

            """, ( data["tracking_number"],data["center_id"],  data["date"], id ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Updated"}), 201