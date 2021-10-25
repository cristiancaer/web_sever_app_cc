from API import create_app
from flask import render_template

app=create_app()

@app.route('/index')
def index():
    return render_template('index.html')