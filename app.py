from flask import Flask, render_template

app = Flask(__name__)

data = [ {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}, {"title": "Test 1", "description": "This is an example description", "tags":{"C++", "Python", "R"}}, {"title": "Test 2", "description": "This is an example description number 2", "tags":{"C++", "Python", "R"}}]   

@app.route("/")
def gallery():
    return render_template('gallery.html', data=data)

@app.route("/submit")
def submit():
    return render_template('form.html')
    
if __name__ == "__main__":
    app.run()
