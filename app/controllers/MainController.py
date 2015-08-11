from flask import render_template
from flask_login import login_required
# app
from app import app


@app.route("/")
# @login_required
def main():
    return render_template('index.html')
