import psycopg2

connect = None
try:
    connect = psycopg2.connect(
        "dbname='linggle_emi' user='atwolin' host='localhost' password='634634634'"
    )
    cursor = connect.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Database version: {db_version}")
    cursor.close()
except Exception as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    if connect:
        connect.close()
        print("PostgreSQL connection is closed")
