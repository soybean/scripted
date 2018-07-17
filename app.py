from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
# from config import *
from app import db, app
from app.models import Project
from flask_mail import Mail, Message

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'melaniensawyer@gmail.com'
app.config['MAIL_PASSWORD'] = 'Clinton23'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.secret_key = 'secret-key'

MAIL_SUBJECT = 'Project Submission Feedback'

@app.route("/")
def gallery():
    query = "SELECT name, id, description, developers from project;"
    result = db.session.execute(query)

    allTags = "SELECT DISTINCT tag,color from tags"
    tagsResult = db.session.execute(allTags)
    allItems = []
    for item in result:
        d = dict(item.items())
        currID = item['id']
        tagsQuery = "SELECT tag,color from tags WHERE projectID = "+str(currID)+";"
        result2 = db.session.execute(tagsQuery)
        d['tags'] = []
        for it in result2:
            d['tags'].append(it)
        allItems.append(d)
    print(allItems)
    return render_template('gallery.html', data=allItems, tags=tagsResult)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form['projectName']
        name = 'TEST PROJECT'
        if name:
            try:
                db.session.add(Project(name=name))
                db.session.commit()
                db.session.close()
                print("1")
                return json.dumps({'html':'<span>Project Added</span>'})
            except Exception as e:
                db.session.rollback()
                print("2")
                print(e)
                return json.dumps({'error':str(e)})
        else:
            print("3")
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    else:
        print("4")
        return render_template('form.html')

# Database functions

# Admin panel function
# POST request if admin is approving, denying, or deleting a project.
@app.route("/adminPanel", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        feedbacktext = request.form['myform']
        # feedback was submitted
        if (feedbacktext):
            feedbackToSend = request.form['feedbackform']
            msg = Message(MAIL_SUBJECT,
                          sender='melaniensawyer@gmail.com',
                          recipients=['melaniensawyer@gmail.com'])
            msg.body = feedbackToSend
            mail.send(msg)

        reject = request.args.getlist('reject')
        delete = request.args.getlist('delete')
        approve = request.args.getlist('approve')

    if 'user' in session:
        return render_template('adminView.html', data=otherdata)
    else:
        return redirect(url_for('login'))

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['user']='admin'
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)


@app.route('/adminAction/<int:reject>', methods=['POST'])
def adminAction(reject):
    print(reject)


if __name__ == "__main__":
    app.run()

