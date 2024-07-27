from flask import Flask, request
from rlm import get_report_data, export_report

app = Flask(__name__)

@app.route("/")
def get_report_data():
    request = request.args.get('request')
    return get_report_data(request)

@app.route("/export")
def export_report():
    data = request.args.get('request')
    type = request.args.get('type')
    return export_report(data, type)
 
if __name__ == '__main__': 
   app.run()
