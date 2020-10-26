import datetime
import json
# from secret import SERVER_KEY, CLIENT_KEY
import os

from flask import Flask, jsonify, render_template, request
from midtransclient import CoreApi, Snap

SERVER_KEY=os.environ['SERVER_KEY']
CLIENT_KEY=os.environ['CLIENT_KEY']


app = Flask(__name__)

#==============#
# Using SNAP
#==============#

# Very simple Snap checkout
@app.route('/simple_checkout')
def simple_checkout():
    snap = Snap(
        is_production=False,
        server_key=SERVER_KEY,
        client_key=CLIENT_KEY,
    )
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = snap.create_transaction({
        "transaction_details": {
            "order_id": "order-id-python-"+timestamp,
            "gross_amount": 210000
        },
        "user_id": 11,
        "customer_details": {
            "first_name": "TEST",
            "last_name": "MIDTRANSER",
            "email": "test@midtrans.com",
            "phone": "+628123456",
            "billing_address": {
                "first_name": "TEST",
                "last_name": "MIDTRANSER",
                "email": "test@midtrans.com",
                "phone": "081 2233 44-55",
                "address": "Sudirman",
                "city": "Jakarta",
                "postal_code": "12190",
                "country_code": "IDN"
            },
        },
        "credit_card": {
            "secure": True,
            "channel": "migs",
            "save_card": True,
            "bank": "bca",
            "installment": {
                "required": False,
                "terms": {
                "bni": [3, 6, 12],
                "mandiri": [3, 6, 12],
                "cimb": [3],
                "bca": [3, 6, 12],
                "offline": [6, 12]
                }
            },
            "whitelist_bins": [
                    "48111111",
                    "41111111"
                ]
        }
    })
    return render_template('simple_checkout.html',
        token = transaction['token'],
        client_key = snap.api_config.client_key,
        transaction=transaction)

@app.route('/notif', methods=["POST"])
def receive_notif():
    data = request.json
    app.logger.warning(f"{data}")

    return jsonify(data)

@app.route('/notif/recurr', methods=["POST"])
def recurr_notif():
    data = request.json
    app.logger.warning(f"{data}")

    return jsonify(data)

# @app.route('/notif/recurr', methods=["POST"])
# def recurr_notif():
#     data = request.json
#     app.logger.warning(f"{data}")

#     return jsonify(data)

@app.route('/finish')
def finish_redir():
    return render_template('finish.html')

@app.route('/unfinish')
def unfinish_redir():
    return render_template('unfinish.html')

@app.route('/error')
def error_redir():
    return render_template('error.html')

#==============#
# Run Flask app
#==============#

# Homepage of this web app
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
