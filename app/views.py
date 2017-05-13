from app import app
from flask import render_template, request


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def proj_about():
    return render_template('about.html')

@app.route('/strategy')
def proj_strategy():
    return render_template('strategy.html')

@app.route('/results')
def proj_results():
    return render_template('results.html')
