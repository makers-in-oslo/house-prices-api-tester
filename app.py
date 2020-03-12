from wtforms import SubmitField, TextField, TextAreaField, RadioField, BooleanField
import json
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
import pandas as pd
from flask import Flask, render_template, send_file, make_response
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
URL_PROD = "https://house-price-prod.herokuapp.com/"
URL_DEV = "https://house-price-staging.herokuapp.com/"


class HouseForm(FlaskForm):
    CRIM = TextField("CRIM: ")
    ZN = TextField("ZN: ")
    INDUS = TextField("INDUS: ")
    CHAS = TextField("CHAS: ")
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
            "CRIM": house_form.CRIM.data,
            "ZN": house_form.ZN.data,
            "INDUS": house_form.INDUS.data,
            "CHAS": house_form.CHAS.data,
            "NOX": house_form.NOX.data,
            "RM": house_form.RM.data,
            "AGE": house_form.AGE.data,
            "DIS": house_form.DIS.data,
            "RAD": house_form.RAD.data,
            "TAX": house_form.TAX.data,
            "PTRATIO": house_form.PTRATIO.data,
            "B": house_form.B.data,
            "LSTAT": house_form.LSTAT.data,
        }
        # print(f"body {body}")
        # print(type(house_form.send_to_dev.data))
        # print(house_form.send_to_dev.data)

        # print(f"send to prod {bool(house_form.send_to_prod.data)}")
        # print(f"send to dev {bool(house_form.send_to_dev.data)}")
        response_dev = False
        response_prod = False
        if (
            house_form.send_to_dev.data & house_form.send_to_prod.data
        ):  # sum(house_form.send_to_dev + house_form.send_to_prod)==0:
            response_dev = requests.request(
                "POST", URL_DEV, data=json.dumps(body), headers=HEADERS
            )
            response_prod = requests.request(
                "POST", URL_PROD, data=json.dumps(body), headers=HEADERS
            )
        elif house_form.send_to_dev.data:
            response_dev = requests.request(
                "POST", URL_DEV, data=json.dumps(body), headers=HEADERS
            )
        elif house_form.send_to_prod.data:
            response_prod = requests.request(
                "POST", URL_PROD, data=json.dumps(body), headers=HEADERS
            )
        else:
            # raise som error
            print("Send to either development or production endpoint")
        html_data = {
            "dev": house_form.send_to_dev.data,
            "prd": house_form.send_to_prod.data,
            "r_dev": response_dev if response_dev else False,
            "r_prod": response_prod if response_dev else False,
            "house_form": house_form,
        }
        print(f"response_dev{response_dev}")
        # print(f"response_dev{response_dev}")

        return render_template("index.html", **html_data)
    return render_template("index.html", house_form=house_form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
