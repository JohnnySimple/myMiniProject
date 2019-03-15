from flask import render_template, url_for, flash, redirect, request
from project import app
from project import db


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html", title="Home")

@app.route('/lecturer_home')
def lecturer_home():
	return render_template("lecturer_home.html", title="Lecturer Home")


@app.route('/admin')
def admin():
	return render_template("admin")