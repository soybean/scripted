from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
# from config import *
from app import db, app
from app.models import Project
from flask_mail import Mail, Message

app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
db = SQLAlchemy(app)

app.secret_key = 'secret-key'

CONFIRMATION_MAIL_SUBJECT = 'ScriptEd Project Submission Confirmation'
CONFIRMATION_MAIL_SENDER = 'cyntzhou@gmail.com'
CONFIRMATION_MAIL_BODY = "This is to confirm that you've submitted \
    a project for ScriptEd. We will email you if your project has \
    been approved."

FEEDBACK_MAIL_SUBJECT = 'Project Submission Feedback'
FEEDBACK_MAIL_SENDER = 'melaniensawyer@gmail.com'

@app.route("/")
def gallery():
    query = "SELECT name, id, description, developers from project;"
    result = db.session.execute(query)

    allTags = "SELECT DISTINCT tag from tags"
    tagsResult = db.session.execute(allTags)
    allItems = []
    for item in result:
        d = dict(item.items())
        currID = item['id']
        tagsQuery = "SELECT tag from tags WHERE projectID = "+str(currID)+";"
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
        # name = request.form['projectName']
        name = 'TEST PROJECT'
        if name:
            try:
                db.session.add(Project(name=name))
                db.session.commit()
                db.session.close()

                email = Message(subject=CONFIRMATION_MAIL_SUBJECT,
                                body=CONFIRMATION_MAIL_BODY,
                                sender=CONFIRMATION_MAIL_SENDER,
                                # recipients=[request.form['email']])
                                recipients=['cyntzhou@gmail.com'])
                print("Mail!!")
                mail.send(email)
                print("mail sent!")
                return json.dumps({'html':'<span>Project Added</span>'})
            except Exception as e:
                db.session.rollback()
                print("angery")
                print(str(e))
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
            msg = Message(FEEDBACK_MAIL_SUBJECT,
                          sender=FEEDBACK_MAIL_SENDER,
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
    app.run(debug=True)
