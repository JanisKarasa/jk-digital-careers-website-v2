# here we write some code to connect to the database and extract some data from it by using SQLAlchemy library - DB Toolkit for Python...
# recourses - https://docs.sqlalchemy.org/

# 1. first install - 'pip install sqlalchemy' then import necessary modules that will be needed writing the code ...
from sqlalchemy import create_engine, text

# 4. import 'os' module to access the environment variables in .env file 
import os
# 4.a import load_dotenv module
from dotenv import load_dotenv
# 4.b take environment variables from .env
load_dotenv()

# 2. next - establish connectivity by creating an 'engine' which is going to connect with database
# all the info we get from PlanetScale's connection (with General) parameters (database:, username:, host:, password:) we provide in a special format ...
# 4.c access and assign an environment variable from .env by use 'os.getenv('...')'
db_connection_string = os.getenv('DB_CONNECTION_STRING')
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
    }
)

# 5. defining function where we connecting with database, getting data, converting and appending in a list of dictionary objects and returning a list
def load_jobs_from_db():
    # 3. getting DB data out of the 'engine' by connecting to it, import our 'engine' module from database.py
    # setting up a connection with engine and giving it a name 'conn', 'with' will close a connection automatically after we finish
    with engine.connect() as conn:
        # connecting and executing query "select * from jobs" then storing it in 'result' (as of type class 'sqlalchemy.engine.cursor.CursorResult')
        result = conn.execute(text("select * from jobs"))
        # creating an empty list where we will store all rows of DB as dictionary objects
        jobs = []
        # retrieving/fetching (result.all()) all the rows as a list of tuple-like objects from the 'result' set returned by executing a SQL query 
        rows = result.all()
        # iterating through the list of rows 
        for row in rows:
            # and converting each row into a dictionary object, and appending to a list making it a list of dictionaries so we can present this data in the website
            jobs.append(row._asdict())
        return jobs
