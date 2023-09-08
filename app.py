from flask import Flask, render_template, jsonify
# importing 'oad_jobs_from_db' function from database.py
from database import load_jobs_from_db

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

if __name__ == "__main__":
    app.run(debug="True")
