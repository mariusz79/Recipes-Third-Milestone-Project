import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo, pymongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'task_manager'
app.config['MONGO_URI'] = os.getenv('MONGO_URI1')  # 'MONGO_URI1' is saved in environment variables, to hide password

mongo = PyMongo(app)

@app.route('/')
def home():
    return 'Hello'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
