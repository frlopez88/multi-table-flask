from flask import Flask, flash , json, jsonify, request
from psycopg2.extras import RealDictCursor
import database


app = Flask(__name__)

## this will create the tables if not exists
database.init_db()

@app.route("/driver")
def get_drivers():
    conn = database.get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
                select * from driver
            """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(rows)
    
@app.route("/driver", methods=["POST"])
def create_driver():
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                insert into driver
                    (license_type, name)
                values (%s, %s)
            """, ( data["license_type"], data["name"] ))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Created"}), 201


@app.route("/driver/<int:id>", methods=["DELETE"])
def delete_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()

    cur.execute("""
                delete from driver where driver_id = %s
            """, ( id, ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Deleted"}), 201


@app.route("/driver/<int:id>", methods=["PUT"])
def update_driver(id):
    conn = database.get_connection()
    cur = conn.cursor()
    data = request.get_json()
    cur.execute("""
                
                update driver 
                set license_type = %s, 
                    name = %s
                where driver_id = %s 

            """, ( data["license_type"],data["name"],  id ))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Object Updated"}), 201

if __name__ == "__main__":
    app.run(debug=True)