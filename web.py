#!/usr/bin/env python3

import main
import collect

import threading
from flask import Flask, request, render_template

new_message = False
def statut_new_message():
    global new_message
    if new_message == True:
        new_message = False
    return new_message

app = Flask(__name__)

@app.route('/')
def home():
    message, name = collect.get_last_message_from_db()
    temp, sound, percentage_co, number_msg = collect.get_last_value_from_db()
    return render_template("index.html", message = message ,name=name, temperature = round(temp,2), sound = sound, percentage = percentage_co, number = number_msg)

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['text']
    name = request.form['name']
    collect.new_message_in_db(text,name)
    new_message = True
    main.message_lcd()
    temp, sound, percentage_co, number_msg = collect.get_last_value_from_db()
    return render_template("index.html", message=text,name=name, temperature = temp, sound = sound, percentage = percentage_co, number = number_msg)
    
threading.Thread(target=lambda: app.run(host="0.0.0.0",debug=False)).start()
