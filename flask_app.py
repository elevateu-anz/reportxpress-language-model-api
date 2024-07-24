from flask import Flask, request
from rlm import generate_report

app = Flask(__name__)

@app.route("/")
def generate_report():
    request = request.args.get('request')
    return generate_report(request)
 
if __name__ == '__main__': 
   app.run()
