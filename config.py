import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/rtr_crawler_Alchemy.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False