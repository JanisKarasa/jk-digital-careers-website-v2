from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
# importing all function from database.py that's going to be used in our routes
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, load_applications_from_db, load_application_from_db, delete_job_from_db

# importing hCaptcha extension
from flask_hcaptcha import hCaptcha

# import 'os' module to access the environment variables in .env file to use hCaptcha's environment variables
import os
# import load_dotenv module to fetch environment variables for hCaptcha
from dotenv import load_dotenv
# take environment variables from .env
load_dotenv()

app = Flask(__name__)
# In case of hCaptcha, a secret key for an app needs to be set to ensure the security of sessions, user authentication, and other features that rely on secure cookies. 
app.secret_key = os.getenv('APP_SECRET_KEY')

# set the HCAPTCHA_SITE_KEY and HCAPTCHA_SECRET_KEY configuration variables with the values from my hCaptcha account.
app.config['HCAPTCHA_SITE_KEY'] = os.getenv('HCAPTCHA_SITE_KEY')
app.config['HCAPTCHA_SECRET_KEY'] = os.getenv('HCAPTCHA_SECRET_KEY')

# implementation of hCaptcha
hcaptcha = hCaptcha()
hcaptcha.init_app(app)
# then inside of the form you want to protect, include the tag: {{ hcaptcha }}. It will insert the code automatically

# A route that renders about.html page
@app.route("/about")
def about():
    return render_template("about.html")

# Defining a route that loads job data from the database and renders an HTML template with the data.
@app.route("/")
def home():
    # loading fetched DB data as a list of dictionaries into variable 'jobs'
    jobs = load_jobs_from_db()
    # by providing argument 'jobs' and passing the value 'jobs' - the list of dictionaries ...
    return render_template("home.html", jobs=jobs)
# ... we can pass fetched DB data into the home.html template by inserting {{jobs}} into HTML, it is the way to insert DYNAMIC DATA into your HTML and CSS

# A route that renders admin.html page with all the jobs to handle the updates and deletes
@app.route("/admin")
def admin():
    jobs = load_jobs_from_db()
    return render_template("admin.html", jobs=jobs)

# Defining an API route that returns all job data in JSON format.
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)
# instead returning HTML we can also return some JSON by using jsonify() function
# The general convention is to use the route '@app.route("/api/jobs")' to differentiate this route/endpoint from html pages

# Defining a route that displays the details of a specific job based on its ID
@app.route("/job/<id>")
def show_job(id):
    # Call the 'load_job_from_db' function to retrieve a job from the database based on the 'id' provided in the URL.
    job = load_job_from_db(id)

    # if job is None (as it is returning in load_job_from_db(id)), if the job is not present, instead of showing empty information ...
    if not job:
        # ... it returns 'Not Found' and specify an error code
        return "Not Found", 404

    # instead of returning JSON, we render template and pass the 'job' data to it allowing to generate an HTML page that displays the job details
    return render_template("jobpage.html", job=job)

# Defining an API route that returns individual job details in JSON format.
@app.route("/api/job/<id>")
def show_job_json(id):
    job = load_job_from_db(id)
    return jsonify(job)

# Defining a route for submitting job applications based on their ID. It handles form data, performs hCaptcha verification, and inserts application data into the database.
# The route construction we get from url we created in application_form.html form element as an 'action' attribute (<form action="/job/{{job.id}}/apply">)
# Route expects the 'post' method from the form in application_form.html that uses 'post' method to send a request with the form data to a server,
# it expects some data to be posted by the browser, and not send in URL bar, to retrieve it with request.form to do all sorts of things with this data
@app.route("/job/<id>/apply", methods=["post"])
def apply_to_job(id):
    # Retrieve form data submitted via the HTTP POST request.
    # When you ‘post’ by submitting a form, the data is present in request.form
    data = request.form

    # load job by its id so we can display name of the job in application_submitted.html / add job=job in render_template(...)
    job = load_job_from_db(id)

    # hCAPTCHA's verification logic

    if hcaptcha.verify():
        # hCaptcha verification passed
        # call this function to populate/insert the data from the form/application (data = request.form) into db,
        # id argument is used to populate the job_id column in db, and data argument is used to populate the rest of the columns in db
        add_application_to_db(id, data)
        flash('hCaptcha verification passed', 'success')
        # Rendering a template where the form data (as a dictionary) is passed with the name 'application'
        # Additionally, we are passing job description data that we load by its id to use that data in the template too
        return render_template('application_submitted.html', application=data, job=job)

    else:
        # hCaptcha verification failed
        flash('hCaptcha verification failed. Please try again', 'danger')
        return render_template('application_submitted.html', application=data, job=job) 

    # we can do all sorts of things with this info (data):
    # store this ‘data’ in DB (did that)
    # displayed an acknowledgement (did that)
    # send a confirmation email to admin and candidate on application submission (TODO use mailjet.com API)

# an API route that returns all the applications in JSON
@app.route("/api/apps")
def show_applications_json():
    apps = load_applications_from_db()
    return jsonify(apps)

# an API route that returns applications for a specific job
@app.route("/api/apps_by_job/<job_id>")
def show_application_by_job_json(job_id):
    apps_by_job = load_application_from_db(job_id)
    return jsonify(apps_by_job)

# A route that will handle the Deletion of the job posting from the database 
@app.route("/delete-job", methods=['POST'])
def delete_job():
    # Extract data from the request body (taken from form in admin.html)
    job = request.form # ImmutableMultiDict([('job_id', 'x')]) - a special type of dictionary-like object provided by Flask that is immutable
    # Extract the 'id' field from dictionary-like structure containing a single key-value pair
    jobID = job.get('job_id') # Use .get() to safely get the 'id' field without raising an error if it's missing
    # Load the job with the specified 'id' from the database to check if it is not empty (None)
    job_db = load_job_from_db(jobID)
    # Check if the 'job_db' variable is not empty (assuming it should contain database data)
    if job_db is not None:
        # Delete the job from the database
        delete_job_from_db(jobID)
        # Redirect to admin.html and flash the message
        flash('Job deleted successfully!', 'success')
        return redirect(url_for('admin'))

    # If the job with the specified 'id' does not exist, redirect to admin.html and flash the message
    flash('Job not found, invalid job ID!', 'danger')
    return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(debug=True)
