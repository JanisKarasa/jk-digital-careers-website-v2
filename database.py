# here we write some code to connect to the database and extract some data from it by using SQLAlchemy library - DB Toolkit for Python...
# recourses - https://docs.sqlalchemy.org/

# 1. first install - 'pip install sqlalchemy' then import necessary modules that will be needed writing the code ...
from sqlalchemy import create_engine, text

# 2. next - establish connectivity by creating an 'engine' which is going to connect with database
# all the info we get from PlanetScale's connection (with General) parameters (database:, username:, host:, password:) we provide in a special format ...
db_connection_string="mysql+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4"
# here, in string replace following keywords: 'user' with username, 'pass' with password, 'some_mariadb' with host, 'dbname' with database(name)
# and store this string variable in '.env' (Environment Variables) file for safe deployment to the cloud render.com

# here we provide information about how to connect to database, import 'create_engine' module
engine = create_engine(
    # predefined string containing sensitive connectivity credentials
    db_connection_string, 
    # connecting securely to a service/server using the SSL (Secure Sockets Layer) protocol with the file path to a Certificate Authority (CA) certificate file
    connect_args={
        "ssl": {
            # this path we get from PlanetScale's connection (with Python) parameters in main.py tab
            "ca": "/etc/ssl/cert.pem"
        }
    })

# 3. getting some info out of the 'engine', import 'text' module
# setting up a connection with engine and giving it a name 'conn', 'with' will close a connection automatically after we finish
with engine.connect() as conn:
    # connecting and executing query "select * from jobs" then storing it in 'result' (as of type class 'sqlalchemy.engine.cursor.CursorResult')
    result = conn.execute(text("select * from jobs"))
    print("type(result): ", type(result))
    # creating an empty list where we will store all rows of DB as dictionary objects
    result_dicts = []

    # retrieving/fetching (result.all()) all the rows as a list of tuple-like objects from the 'result' set returned by executing a SQL query 
    rows = result.all()
    
    # iterating through the list of rows 
    for row in rows:
        # and converting each row into a dictionary object, and appending to a list making it a list of dictionaries so we can present this info in the website
        result_dicts.append(row._asdict())
    # for now printing a list of dictionary objects in our console
    print(result_dicts)
