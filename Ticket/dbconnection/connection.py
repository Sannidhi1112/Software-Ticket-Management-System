#this file we setsup the connectio to the db.
#intialize it wit the mysql connector . 
#Change username and password as your SQL
import mysql.connector;

def connect(username,pwd,db):
    conn = mysql.connector.connect(host="localhost",user="root",password="Sharan@0201",database=db);
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    return conn,cursor;

def query_data_select(sqlstmt,conn,cursor):
    # Execute a simple query
    cursor.execute(sqlstmt)
    # Fetch the results
    results = cursor.fetchall()
    
    return results;
    # Close the cursor and connection
    # cursor.close()
    # conn.close()


def insert_data(sqlstmt,conn,cursor):
    print(sqlstmt);
    cursor.execute(sqlstmt);
    conn.commit();
    return True;