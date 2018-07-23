from flask import Flask, render_template, json, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
# from config import *
from app import db, app
from app.models import Project
from PIL import Image

from flask_debugtoolbar import DebugToolbarExtension
app.debug = True

app.config['SECRET_KEY'] = 'asldfkajsdlfk'

toolbar = DebugToolbarExtension(app)

# app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
db = SQLAlchemy(app)

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
    query = "SELECT name, id, description, developers,screenshot from project WHERE status='approved' AND isDeleted='false';"
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

        if name and screenshot and num_developers and developers and \
            description and long_description and program_attended and email:
            try:
                # print("!!!!!!!!!!")
                db.session.add(Project(name=name,
                                       screenshot=screenshot,
                                       num_developers=num_developers,
                                       developers=developers,
                                       github_usernames=github_usernames,
                                       description=description,
                                       link=link,
                                       github_repo=github_repo,
                                       long_description=long_description,
                                       program_attended=program_attended,
                                       email=email,
                                       status="pending",
                                       isDeleted='false'
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
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    else:
        allTags = "SELECT DISTINCT tag,color from tags"
        tagsResult = db.session.execute(allTags)
        return render_template('form.html', tags=tagsResult)

# Database functions

# Admin panel function
# POST request if admin is approving, denying, or deleting a project.
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        feedbacktext = request.form['myform']
        # feedback was submitted
        if (feedbacktext):
            print("RECEIEVED")
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
        query = "SELECT * FROM project WHERE isDeleted='false';"
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



@app.route('/delete', methods=["POST"])
def delete():
    myID = request.form['id_to_delete']
    db.session.query(Project).filter(Project.id==myID).update({'isDeleted': 'true'})
    db.session.commit()
    db.session.close()
    return(redirect(url_for('admin')))

@app.route('/approve', methods=['POST'])
def approve():
    myID = request.form['id_to_approve']
    db.session.query(Project).filter(Project.id==myID).update({'status':'approved'})
    db.session.commit()
    db.session.close()
    return(redirect(url_for('admin')))

@app.route('/feedback', methods=['POST'])
def feedback():
    myID = request.form['id_to_give_feedback']
    db.session.query(Project).filter(Project.id==myID).update({'status':'feedback'})
    db.session.commit()
    db.session.close()
    print("heelo...")
    return(redirect(url_for('admin')))

@app.route('/project/<id>', methods=['GET'])
def project(id):
    query = "SELECT * FROM project WHERE id="+id+";"
    result = db.session.execute(query).first();
    d = dict(result)
    currentID = d['id']
    tagsQuery = 'SELECT tag,color from tags WHERE projectID= ' + str(currentID) + ";"
    tagsResult = db.session.execute(tagsQuery)
    d['tags']=[]
    for item in tagsResult:
        d['tags'].append(item)
    print(d['tags'])
    return(render_template('project2.html', data=d))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
