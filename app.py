from wtforms import SubmitField, TextField, TextAreaField, RadioField, BooleanField
import json
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import pandas as pd
from flask import Flask, render_template, send_file, make_response, url_for
import pickle
import base64
import numpy as np
import requests


app = Flask(__name__)
app.secret_key = "Må byttes ut før GO-live"
COLUMNS = [
    "CRIM",
    "ZN",
    "INDUS",
    "CHAS",
    "NOX",
    "RM",
    "AGE",
    "DIS",
    "RAD",
    "TAX",
    "PTRATIO",
    "B",
    "LSTAT",
]
HEADERS = {"Content-Type": "application/json"}
URL_PROD_B = "https://house-price-prod.herokuapp.com/bjornar"
URL_PROD_D = "https://house-price-prod.herokuapp.com/daniel"
URL_DEV_B = "https://house-price-staging.herokuapp.com/bjornar"
URL_DEV_D = "https://house-price-staging.herokuapp.com/daniel"


class HouseForm(FlaskForm):
    CRIM = TextField("CRIM: ")
    ZN = TextField("ZN: ")
    INDUS = TextField("INDUS: ")
    CHAS = BooleanField("CHAS: ")
    NOX = TextField("NOX: ")
    RM = TextField("RM: ")
    AGE = TextField("AGE: ")
    DIS = TextField("DIS: ")
    RAD = TextField("RAD: ")
    TAX = TextField("TAX: ")
    PTRATIO = TextField("PTRATIO: ")
    B = TextField("B: ")
    LSTAT = TextField("LSTAT: ")
    send_to_prod = BooleanField("send to production")
    send_to_dev = BooleanField("send to devlopment")
    sumbit = SubmitField("Submit choices")


@app.route("/", methods=["GET", "POST"])
def init():
    house_form = HouseForm()
    if house_form.validate_on_submit():
        body = {
            "CRIM": float(house_form.CRIM.data),
            "ZN": float(house_form.ZN.data),
            "INDUS": float(house_form.INDUS.data),
            "CHAS": float(house_form.CHAS.data == "True"),
            "NOX": float(house_form.NOX.data),
            "RM": float(house_form.RM.data),
            "AGE": float(house_form.AGE.data),
            "DIS": float(house_form.DIS.data),
            "RAD": float(house_form.RAD.data),
            "TAX": float(house_form.TAX.data),
            "PTRATIO": float(house_form.PTRATIO.data),
            "B": float(house_form.B.data),
            "LSTAT": float(house_form.LSTAT.data),
        }
        response_dev_b = False
        response_dev_d = False
        response_prod_b = False
        
        response_prod_d = False
        if house_form.send_to_dev.data & house_form.send_to_prod.data:
            response_dev_b = requests.request(
                "POST", URL_DEV_B, data=json.dumps(body), headers=HEADERS
            )
            response_dev_d = requests.request(
                "POST", URL_DEV_D, data=json.dumps(body), headers=HEADERS
            )
            response_prod_b = requests.request(
                "POST", URL_PROD_B, data=json.dumps(body), headers=HEADERS
            )
            response_prod_d = requests.request(
                "POST", URL_PROD_D, data=json.dumps(body), headers=HEADERS
            )
        elif house_form.send_to_dev.data:
            response_dev_b = requests.request(
                "POST", URL_DEV_B, data=json.dumps(body), headers=HEADERS
            )
            response_dev_d = requests.request(
                "POST", URL_DEV_D, data=json.dumps(body), headers=HEADERS
            )
        elif house_form.send_to_prod.data:
            response_prod_b = requests.request(
                "POST", URL_PROD_B, data=json.dumps(body), headers=HEADERS
            )
            response_prod_d = requests.request(
                "POST", URL_PROD_D, data=json.dumps(body), headers=HEADERS
            )
        else:
            # raise som error
            print("Send to either development or production endpoint")
        html_data = {
            "dev": house_form.send_to_dev.data,
            "prod": house_form.send_to_prod.data,
            "r_dev_b": decode_content(get_content(response_dev_b)),
            "r_dev_d": decode_content(get_content(response_dev_d)),
            "r_prod_b": decode_content(get_content(response_prod_b)),
            "r_prod_d": decode_content(get_content(response_prod_d)),
            "house_form": house_form,
        }
        return render_template("index.html", **html_data)
    return render_template("index.html", house_form=house_form)


def get_content(response):
    try:
        response = response.content
    except AttributeError:
        response = False

    return response


def decode_content(content):
    try:
        decoded_content = content.decode("utf-8").replace("\\", "")
    except AttributeError:
        decoded_content = "no content"
    return decoded_content


if __name__ == "__main__":
    app.run(debug=True, port=5001)
