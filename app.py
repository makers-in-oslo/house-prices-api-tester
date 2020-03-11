
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
HEADERS = {'Content-Type': 'application/json'}
URL_PROD = "https://house-price-prod.herokuapp.com/"
URL_DEV = "https://house-price-staging.herokuapp.com/"
class HouseForm(FlaskForm):
    var1 = TextField("var1: " )
    var2 = TextField("var2: ") 
    var3 = TextField("var3: ") 
    var4 = TextField("var 4: ") 
    var5 = TextField("var 5: ") 
    var6  = TextField("var 6: ") 
    var7 = TextField("var7: ") 
    send_to_prod = BooleanField("send to production")
    send_to_dev = BooleanField("send to devlopment")
    sumbit = SubmitField("Submit choices")


@app.route("/", methods=["GET", "POST"])
def init():
    house_form = HouseForm()
    if house_form.validate_on_submit():
        body = {'var1': house_form.var1.data,
        'var2': house_form.var2.data,
        'var3': house_form.var3.data,
        'var4': house_form.var4.data,
        'var5': house_form.var5.data,
        'var6': house_form.var6.data,
        'var7': house_form.var7.data
        }
        if house_form.send_to_dev & house_form.send_to_prod: #sum(house_form.send_to_dev + house_form.send_to_prod)==0:
            response_dev = requests.request("POST", URL_DEV, data=str(body), headers=HEADERS)
            response_prod = requests.request("POST", URL_PROD, data=str(body), headers=HEADERS)
        elif house_form.send_to_dev:
            response_dev = requests.request("POST", URL_DEV, data=str(body), headers=HEADERS)
        elif house_form.send_to_prod:
            response_prod = requests.request("POST", URL_PROD, data=str(body), headers=HEADERS)
        else: 
            #raise som error
            print("Send to either development or production endpoint")
        html_data = {'r_dev':response_dev if response_dev else None,
                     'r_prod': response_prod if response_dev else None,
                     'house_form':house_form}
        return render_template("index.html", **html_data, {})
    return render_template("index.html", house_form = house_form)

