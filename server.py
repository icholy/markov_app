#!/usr/bin/env python

import sqlite3
import pandas
import re
import markovify
from flask import Flask, render_template, send_from_directory, request

all_users = [
    "Brandon Rosier",
    "Caroline Kupka",
    "Christopher Daniel",
    "Claire",
    "Deven Gelinas",
    "Dylan St Onge",
    "Ilia Choly",
    "John Clare",
    "Kaitlin Labatte",
    "Kate DeGasperis",
    "Kelsey Kaupp",
    "Lindsey Brown",
    "Mark Meleka",
    "Mike Edward",
    "Mike Oligradskyy",
    "Nate Fawcett",
    "Nick Felice",
    "Olivia Bullock",
    "Pola Kurzydlo",
    "Sarah Ollikainen",
    "Sarah Ross",
    "Sean Haine",
    "Steven Murphy",
    "Thomas Gabriele",
    "Tom Bonomi"
]

url_regex = re.compile(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def clean_text(text):
    text = text.lower()
    text = email_regex.sub("", text)
    text = url_regex.sub('', text)
    text = text.replace("'", "")
    text = re.sub(r'[^A-Za-z0-9]+', ' ', text)
    text = re.sub(r'[\(\)\#\%\-\$\'\!\?\,\:\/\_\s\=\^\<\+\@]+', ' ', text)
    text = text.replace(".", "\n")
    return text

def create_makrov_models():
    with sqlite3.connect("messages.db") as conn:
        df = pandas.read_sql_query("select * from messages", conn)
        models = {}
        for user in all_users:
            print "Creating Model For: {0}".format(user)
            df.text = df.text.map(clean_text)
            raw_text = "\n".join(df[df.user == user]["text"])
            model = markovify.NewlineText(raw_text)
            models[user] = model
        return models

app = Flask(__name__)
user_models = create_makrov_models()

def make_sentence(users):
    models = []
    for user in users:
        if user in user_models:
            models.append(user_models[user])
    combined_model = markovify.combine(models)
    return combined_model.make_sentence(tries=100)

@app.route("/generate_sentence")
def generate_sentence():
    users = request.args.getlist('u[]')
    sentence = make_sentence(users)
    if not sentence:
        sentence = "Error: failed to build chain"
    return sentence

@app.route("/")
def index():
    return render_template("index.html", users = all_users)

@app.route('/assets/<path:path>')
def assets(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


