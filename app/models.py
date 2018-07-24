from app import db
from sqlalchemy.dialects.sqlite import BLOB

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=False)
    screenshot = db.Column(db.String(1000), index=True, unique=False)
    num_developers = db.Column(db.Integer, index=True, unique=False)
    developers = db.Column(db.String(400), index=True, unique=False)
    github_usernames = db.Column(db.String(400), index=True, unique=False)
    description = db.Column(db.String(200), index=True, unique=False)
    link = db.Column(db.String(100), index=True, unique=False)
    github_repo = db.Column(db.String(100), index=True, unique=False)
    long_description = db.Column(db.String(4000), index=True, unique=False)
    program_attended = db.Column(db.String(100), index=True, unique=False)
    email = db.Column(db.String(100), index=True, unique=False)
    status = db.Column(db.String(30), index=True, unique=False)
    isDeleted = db.Column(db.String(100), index=True, unique=False)

    def __init__(self, name, screenshot, num_developers, developers, \
     github_usernames, description, link, github_repo, long_description, \
     program_attended, email, status):
        self.name = name
        self.screenshot = screenshot
        self.num_developers = num_developers
        self.developers = developers
        self.github_usernames = github_usernames
        self.description = description
        self.link = link
        self.github_repo = github_repo
        self.long_description = long_description
        self.program_attended = program_attended
        self.email = email
        self.status = status

    def __repr__(self):
        return '<Project (name=%s)>' % (self.name)
        # return '<Project (name=%s, description=%s)>' % (self.name, self.description)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), index=True, unique=False)
    projectID = db.Column(db.Integer, index=True, unique=False)
    color =  db.Column(db.String(30), index=True, unique=False)

    def __init__(self, tag, projectID):
        tag_colors = {
            'Python': '#4286f4',
            'JavaScript': '#00b515',
            'HTML': '#f94600',
            'Java': '#ff0061',
            'CSS': '#8d05ba',
            'Beginner': '#00e082',
            'Intermediate': '#d1c300',
            'Advanced': '#d10000'
        }

        self.tag = tag
        self.projectID = projectID
        if tag in tag_colors:
            self.color = tag_colors[tag]
        else:
            self.color = 'grey'
