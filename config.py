import credentials

# format: (user):(password)@(db_identifier).amazonaws.com:3306/(db_name)
DB_USER = credentials.DB_USER
DB_PASSWORD = credentials.DB_PASSWORD
DB_NAME = credentials.DB_NAME
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@scripted.csi6qpe1wnpo.us-east-2.rds.amazonaws.com:3306/%s' % (DB_USER, DB_PASSWORD, DB_NAME)

# Uncomment the line below if you want to work with a local DB
# SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600
WTF_CSRF_ENABLED = True
