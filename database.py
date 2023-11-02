# here we write some code to connect to the database using SQLAlchemy library - DB Toolkit for Python...
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
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    }
)

# 5. Defining a function where we connecting with database, getting all data from jobs table, converting and appending in a list of dictionary objects and returning a list
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


# 6. Define a function that takes an 'id' as an argument.
def load_job_from_db(id):
    # Open a connection to the database using the 'engine'.
    with engine.connect() as conn:
        # Execute an SQL query that selects all columns from the 'jobs' table where 'id' matches the provided value.
        # The ':val' is a named parameter that will be replaced by the value of 'id'.
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
            {"val": id}  # Use a dictionary to bind the 'id' parameter
        )
        
        # Fetch all rows from the result set and store them in the 'rows' list.
        rows = result.all() 
        
        # Check if there are no rows in the result set (empty result).
        if len(rows) == 0:
            # If no rows are found, return None to indicate that no job was found with the given 'id'.
            return None
        else:
            # If rows are found, convert the first row to a dictionary using '_asdict()' method.
            # This allows you to represent the row as a dictionary where column names are keys.
            # Return the dictionary representation of the first row.
            return rows[0]._asdict()

#7. Defining a function where we connecting with database to insert the data in db from application forms based on job id
def add_application_to_db(job_id, application):
    # Establish a connection to the database using the 'engine' object.
    with engine.connect() as conn:
        # Define an SQL query using SQLAlchemy's 'text' function to insert data into the 'applications' table.
        query = text( "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
        
        # Execute the SQL query by passing a dictionary of parameter values.
        conn.execute(query, 
                     {"job_id": job_id,
                      "full_name": application["full_name"],
                      "email": application["email"],
                      "linkedin_url": application["linkedin_url"],
                      "education": application["education"],
                      "work_experience": application["work_experience"],
                      "resume_url": application["resume_url"]})
        
# 8. Load all applications from db
def load_applications_from_db():
    with engine.connect() as conn:
        # Execute an SQL query that selects all columns from the 'applications' table
        result = conn.execute(text("SELECT * FROM applications"))
        # creating an empty list where we will store all rows of DB 'applications' table as dictionary objects
        applications = []
        # Fetch all rows from the result set and store them in the 'rows' list.
        rows = result.all()
        # iterating through the list of rows 
        for row in rows:
            # and converting each row into a dictionary object, and appending to a list making it a list of dictionaries so we can present this data in the website
            applications.append(row._asdict())
        return applications

# 9. Load an individual application for a specific job 
def load_application_from_db(job_id):
    # Open a connection to the database using the 'engine'.
    with engine.connect() as conn:
        # Execute an SQL query that selects all columns from the 'jobs' table where 'id' matches the provided value.
        # The ':val' is a named parameter that will be replaced by the value of 'id'.
        result = conn.execute(
            text("SELECT * FROM applications WHERE job_id = :val"),
            {"val": job_id}  # Use a dictionary to bind the 'id' parameter
        )
        
        # Fetch all rows from the result set and store them in the 'rows' list.
        rows = result.all() 
        
        # Check if there are no rows in the result set (empty result).
        if len(rows) == 0:
            # If no rows are found, return None to indicate that no job was found with the given 'id'.
            return None
        else:
            applications = []

            for row in rows:
                applications.append(row._asdict())
            return applications

# Delete the job from database
def delete_job_from_db(id):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM jobs WHERE id = :val"),
            {"val": id}  # Use a dictionary to bind the 'id' parameter
        )

# Add the job to a database
def add_job_to_db(job):
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)"),
            {
                "title": job["job_title"],
                "location": job["job_location"], 
                "salary": job["job_salary"], 
                "currency": job["job_currency"], 
                "responsibilities": job["job_responsibilities"], 
                "requirements": job["job_requirements"]
            }
        )

# Update the job posting
def update_job_in_db(job_id, new_job_data):
    with engine.connect() as conn:
        conn.execute(
            text("UPDATE jobs SET title = :title, location = :location, salary = :salary, currency = :currency, responsibilities = :responsibilities, requirements = :requirements WHERE id = :job_id"),
            {
            "title": new_job_data["job_title"],
            "location": new_job_data["job_location"],
            "salary": new_job_data["job_salary"],
            "currency": new_job_data["job_currency"],
            "responsibilities": new_job_data["job_responsibilities"],
            "requirements": new_job_data["job_requirements"],
            "job_id": job_id
            }
        )

# Inject Dummy Data into the database
def add_dummy_jobs_to_db():
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) " + 
                 "VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)"),
            {
                "title": "Data Analyst",
                "location": "San Francisco", 
                "salary": "100000", 
                "currency": "USD", 
                "responsibilities": "Process data using Python, SQL and other tools through the analytics data pipeline \r\nIdentify and translate business rules into specifications and documentation \r\nEnsure quality control and follow peer review guidelines \r\nAdhere to best practices and standards, maintaining process efficiencies", 
                "requirements": "Bachelor's degree (required) or above in Computer Science, Mathematics, Economics, or experience in related analytical field \r\nExcellent analytic and creative problem-solving skills \r\n1-3 years Python and SQL programming experience \r\nBasic skills in MS Excel Knowledge of cloud computing platforms (AWS, GCP) and knowledge of Spark is desired",
            })
        conn.execute(
            text("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) " + 
                 "VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)"),
            {
                "title": "Data Scientist",
                "location": "Paris, France", 
                "salary": "140000", 
                "currency": "EUR", 
                "responsibilities": "Draft detailed scope for assigned projects, Addressing suggested methodology and execution framework \r\nExecute on the plan with appropriate data mining, analytical and data science techniques \r\nPerform quality assurance of data and deliverables for work performed by other Data Scientists, Data Engineers and self \r\nAccountable for the quality of the end solution or model by planning the required reviews on code and process.", 
                "requirements": "Expert knowledge in Deep Learning techniques and exploring newer approaches like federated learning and transfer learning \r\nProficient in some or all of the following techniques: Linear & Logistic Regression, Decision Trees, Random Forests, K-Nearest Neighbors, Markov Chain, Monte Carlo, Gibbs Sampling, Evolutionary Algorithms, Support Vector Machines \r\nProficient in advanced data mining and statistical modeling techniques, including Predictive modeling"
            }
        )
        conn.execute(
            text("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) " + 
                 "VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)"),
            {
                "title": "Backend Engineer",
                "location": "London, UK", 
                "salary": None, 
                "currency": None, 
                "responsibilities": "Design and develop a cloud based backend \r\nParticipate and produce a scalable cloud based backend system \r\nDesign and develop REST based APIs \r\nInteract with customer directly and with other stakeholders in the organization", 
                "requirements": "Hands on experience with building a web backend in Java or Golang \r\nKnowledge of designing and building REST APIs \r\nProven experience in building a scalable and resilient backend \r\nGood understanding of database schemas and using both relational (SQL) and noSQL based data stores \r\nStrong analytical and debugging skills"
            }
        )
        conn.execute(
            text("INSERT INTO jobs (title, location, salary, currency, responsibilities, requirements) " + 
                 "VALUES (:title, :location, :salary, :currency, :responsibilities, :requirements)"),
            {
                "title": "Frontend Engineer",
                "location": "New Delhi, India", 
                "salary": "1200000", 
                "currency": "Rs", 
                "responsibilities": "Translate designs and wireframes into high quality JS, CSS, HTML templates \r\nDesign, build, and maintain high performance, reusable, and reliable UI components and products \r\nEnsure the best possible performance, quality, and optimize for maximum speed and scalability \r\nIdentify and correct bottlenecks and fix bugs. \r\nHelp maintain code quality, organization, and automatization.", 
                "requirements": "Strong knowledge of programming skills in JS, CSS and HTML \r\nFamiliarity with responsive and adaptive web design, and good knowledge of JS libraries such as jQuery \r\nStrong knowledge of about at least one of the JS frameworks (e.g. VueJS, Angular JS, NodeJS, ReactJS) \r\nExperience with building websites, ability to handle cross browser compatibility issues"
            }
        )