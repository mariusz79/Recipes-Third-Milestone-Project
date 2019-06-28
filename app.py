import os
from flask import Flask, render_template, redirect, request, url_for, flash, session

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello'


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)