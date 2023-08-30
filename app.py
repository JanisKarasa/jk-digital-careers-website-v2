from flask import Flask, render_template

app = Flask(__name__)

# Dummy Database
JOBS = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'San Francisco, USA',
        'salary': "100 000 USD"
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Remote',
        'salary': "170 000 EUR"
    },
    {
        'id': 3,
        'title': 'Backend Engineer',
        'location': 'London, UK',
        # salary is not listed for this role and we handling that with 'if' statement in logic in our home.html 
    },
    {
        'id': 4,
        'title': 'Frontend Engineer',
        'location': 'New Delhi, India',
        'salary': "Rs 12,00,000"
    },
]
# and we send this information into the home.html template by providing arguments into render_templates


@app.route("/")
def home():
    # by providing argument 'jobs' and passing the value 'JOBS' the list of dictionaries ...
    return render_template("home.html", jobs=JOBS)
# ... we can send this information into the home.html template by inserting {{jobs}} into HTML
# it is the way to insert DYNAMIC DATA into your HTML and CSS

if __name__ == "__main__":
    app.run(debug=True)
