import mysql.connector;
from streamlit_extras.switch_page_button import switch_page
# Establish a connection to the MySQL server
#Change username and password as your SQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sharan@0201",
    database="softwareticketmanagement"
)

switch_page("Login")