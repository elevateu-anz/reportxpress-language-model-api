from flask import Flask, request
from rlm import get_report_data

app = Flask(__name__)

@app.route("/")
def get_report_data():
    request = request.args.get('request')
    return get_report_data(request)
 
if __name__ == '__main__': 
   app.run()
