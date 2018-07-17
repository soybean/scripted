from flask import Flask, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
# from config import *
from app import db, app
from app.models import Projects

from PIL import Image

# app.debug = True
app.secret_key = 'bunnies'

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

data = [ {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}]

@app.route("/")
def gallery():
    return render_template('gallery.html', data=data)

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
                db.session.add(Projects(name=name, \
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
    app.run(debug=True)
