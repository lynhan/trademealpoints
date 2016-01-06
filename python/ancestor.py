# key.py 
# keys to use for strongly consistent searches
# twizzley 

from google.appengine.ext import db


def feedback_key():
    return db.Key.from_path('feedback_kind', 'feedback_id')

def sell_key():
    return db.Key.from_path('sell_kind', 'sell_id')

def user_key():
    return db.Key.from_path('user_kind', 'user_id')

def verify_key():
    return db.Key.from_path('verify_kind', 'verify_id')
