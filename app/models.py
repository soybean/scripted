from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=False)
    # screenshot = db.Column(db.String(200), index=True, unique=False)
    # description = db.Column(db.String(200), index=True, unique=False)
    # link = db.Column(db.String(100), index=True, unique=False)
    # github_repo = db.Column(db.String(100), index=True, unique=False)
    # long_description = db.Column(db.String(4000), index=True, unique=False)
    # date = db.Column(db.Date, index=True, unique=False)
    # developers = db.Column(db.String(400), index=True, unique=False)
    # github_usernames = db.Column(db.String(400), index=True, unique=False)

    def __init__(self, name):
        self.name = name
        # self.screenshot = screenshot
        # self.description = description
        # self.link = link
        # self.github_repo = github_repo
        # self.long_description = long_description
        # self.date = date
        # self.developers = developers
        # self.github_usernames = github_usernames

    def __repr__(self):
        return '<Project (name=%s)>' % (self.name)
        # return '<Project (name=%s, description=%s)>' % (self.name, self.description)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(100), index=True, unique=False)  # includes events, classes, skills, etc.

# # How to relate the 2 classes?
# class ProjectsEvents(db.Model):
#     project_id = db.Column(db.Integer)
#     event_id = db.Column(db.Integer)
