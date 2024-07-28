from flask import Flask, request
from rlm import get_report_data, export_report
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_report():
    input = request.args.get('input')
    return get_report_data(input)

@app.route("/export")
def export_report():
    data = request.args.get('data')
    type = request.args.get('type')
    return export_report(data, type) 
 
if __name__ == '__main__': 
   app.run()
