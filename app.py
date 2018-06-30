from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def gallery():
    return render_template('gallery.html')

@app.route("/submit")
def submit():
    return render_template('form.html')
    
if __name__ == "__main__":
    app.run()
