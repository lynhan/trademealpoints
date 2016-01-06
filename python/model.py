# model.py 
# db models
# twizzley 

from google.appengine.ext import db


class UserModel(db.Model):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)

class SellModel(db.Model):
    user = db.ReferenceProperty(UserModel)
    amount = db.StringProperty(required=True)
    price = db.StringProperty(required=True)
    fulfilled = db.BooleanProperty(default=False)
    created = db.DateTimeProperty(auto_now=True)

class FeedbackModel(db.Model):
    feedback = db.TextProperty()

class VerifyModel(db.Model):
    email = db.StringProperty()
    code = db.StringProperty()
