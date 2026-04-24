import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        port =os.getenv("DB_PORT"),
        dbname = os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        sslmode = os.getenv("DB_SSLMODE")
    )

    return conn

def init_db() :
    conn = get_connection()
    cur= conn.cursor()
    cur.execute("""  

            create table if not exists driver
                (
                    driver_id serial primary key ,
                    license_type varchar(250),
                    name varchar(250)
                );
            
            create table if not exists vehicle
                (
                    license_plate varchar(50) primary key,
                    model varchar(250),
                    capacity numeric,
                    driver_id int references driver(driver_id)  unique-- creation to a foreign key
                );
            
            create table if not exists center
                (
                    center_id serial primary key,
                    city varchar(250),
                    manager int references driver(driver_id) unique -- creation to a foreign key
                );

            create table if not exists shipment
                (
                    tracking_number serial primary key ,
                    weight numeric,
                    destination varchar(250),
                    driver_id  int references driver(driver_id)
                );

         """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Database Ready!!! ✅ ")