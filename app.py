from flask import Flask, render_template, jsonify, request
# importing 'oad_jobs_from_db' function from database.py
from database import load_jobs_from_db, load_job_from_db

app = Flask(__name__)


@app.route("/")
def home():
    # loading fetched DB data as a list of dictionaries into variable 'jobs'
    jobs = load_jobs_from_db()
    # by providing argument 'jobs' and passing the value 'jobs' - the list of dictionaries ...
    return render_template("home.html", jobs=jobs)
# ... we can pass fetched DB data into the home.html template by inserting {{jobs}} into HTML
# it is the way to insert DYNAMIC DATA into your HTML and CSS

# this is a second URL/endpoint that's been added to our server as an API
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)
# instead returning HTML we can also return some JSON by using jsonify() function
# this is other way that some websites allow to access some Dynamic Data by using an API. 
# It takes any object stored in variable and converts it into JSON object. It could also be coming from Database
# The general convention is to use the route '@app.route("/api/jobs")' to differentiate this route/endpoint from html pages

# route that will access and display the job description by its id
# This route handles requests to URLs like "/job/<id>", where "<id>" is a dynamic part of the URL.
@app.route("/job/<id>")
def show_job(id):
    # Call the 'load_job_from_db' function to retrieve a job from the database based on the 'id' provided in the URL.
    job = load_job_from_db(id)

    # if job is None (as it is returning in load_job_from_db(id)), if the job is not present, instead of showing empty information ...
    if not job:
        # ... it returns 'Not Found' and specify your error code
        return "Not Found", 404

    # instead of returning JSON, we render template and pass the 'job' data to it
    # This allows you to generate an HTML page that displays the job details
    return render_template("jobpage.html", job=job)

# Define a route for applying to a job with a specific 'id'.
# The route construction we get from url bar when we hit submit (form) button. And we use this construction to create a route.
# And now the route expects the 'post' method from the form in application_form.html that uses 'post' method,
# it expects some data to be posted by the browser, and not send in URL bar, to retrieve it with request.form to do all sorts of things with this data
@app.route("/job/<id>/apply", methods=["post"])
def apply_to_job(id):
    # Retrieve form data submitted via the HTTP POST request.
    # When you ‘post’ by submitting a form, the data is present in request.form
    data = request.form

    # load job by its id so we can display name of the job in application_submitted.html / add job=job in render_template(...)
    job = load_job_from_db(id)

    # we can do all sorts of things with this info (data):
    # store this ‘data’ in DB
    # displayed an acknowledgement 
    # send a confirmation email

    # Instead of returning JSON, we render a template where the form data (as a dictionary) is passed with the name 'application'
    # Additionally, we are passing job description data that we load by its id to use that data in the template too
    return render_template('application_submitted.html', application=data, job=job)

if __name__ == "__main__":
    app.run(debug="True")
