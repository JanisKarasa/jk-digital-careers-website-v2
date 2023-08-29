from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>JK Careers</p>"


# if __name__ == "__name__":
#     app.run(host='0.0.0.0', port=5500, debug=True)
