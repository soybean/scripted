from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
# from config import *
from app import db, app
from app.models import Project

app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Views
@app.route("/")
def gallery():
    return render_template('gallery.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['projectName']
        if name:
            try:
                db.session.add(Project(name=name))
                db.session.commit()
                db.session.close()
                return json.dumps({'html':'<span>Project Added</span>'})
            except Exception as e:
                db.session.rollback()
                return json.dumps({'error':str(e)})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    else:
        return render_template('form.html')

# Database functions

if __name__ == "__main__":
    app.run()
