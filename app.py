from flask import Flask, render_template, json, request
# from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from config import *

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = MYSQL_DATABASE_USER
app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_DATABASE_PASSWORD
app.config['MYSQL_DATABASE_DB'] = MYSQL_DATABASE_DB
app.config['MYSQL_DATABASE_HOST'] = MYSQL_DATABASE_HOST
mysql.init_app(app)

# Views
@app.route("/")
def gallery():
    return render_template('gallery.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            name = request.form['projectName']
            if name:
                add_project(name)
                return json.dumps({'html':'<span>All fields good !!</span>'})
            else:
                return json.dumps({'html':'<span>Enter the required fields</span>'})
        except Exception as e:
            return json.dumps({'error':str(e)})
    else:
        return render_template('form.html')

# Database functions
def add_project(name):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO
            projects (name)
        VALUES (%s)""", (name))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
