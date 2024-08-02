from flask import Flask, request
from rlm import get_report_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_report():
    input = request.args.get('input')
    return get_report_data(input)

if __name__ == '__main__': 
   app.run()
