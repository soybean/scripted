from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
# from config import *
from app import db, app
from app.models import Project
from PIL import Image

# app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
db = SQLAlchemy(app)

# data = [ {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}]
app.secret_key = 'secret-key'

CONFIRMATION_MAIL_SUBJECT = 'ScriptEd Project Submission Confirmation'
CONFIRMATION_MAIL_SENDER = 'cyntzhou@gmail.com'
CONFIRMATION_MAIL_BODY = """
    This is to confirm that you've submitted
    a project for ScriptEd. We will email you if your project has
    been approved.
"""

FEEDBACK_MAIL_SUBJECT = 'Project Submission Feedback'
FEEDBACK_MAIL_SENDER = 'melaniensawyer@gmail.com'

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
        # print ("--------------")
        # print (request.files)
        # print (request.form)

        name = request.form['name']
        if 'screenshot' in request.files:
            f = request.files['screenshot']
            img = Image.open(f)
            path = "static/img/" + f.filename
            img.save(path)
        screenshot = "static/img/" + f.filename
        num_developers = request.form['num_developers']
        developers = request.form['developers']
        github_usernames = request.form['github_usernames']
        description = request.form['description']
        link = request.form['link']
        github_repo = request.form['github_repo']
        long_description = request.form['long_description']
        program_attended = request.form['program_attended']
        email = request.form['email']

        if name:
            try:
                # print("!!!!!!!!!!")
                db.session.add(Project(name=name, \
                                       screenshot=screenshot, \
                                       num_developers=num_developers, \
                                       developers=developers, \
                                       github_usernames=github_usernames, \
                                       description=description, \
                                       link=link, \
                                       github_repo=github_repo, \
                                       long_description=long_description, \
                                       program_attended=program_attended, \
                                       email=email
                                       ))
                # print("???????")
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
@app.route("/admin", methods=['GET', 'POST'])
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
        query = "SELECT * FROM project;"
        result = db.session.execute(query)
        return render_template('adminView.html', data=result)
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

    app.run(port = 4000)

