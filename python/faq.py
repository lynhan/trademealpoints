# faq.py 
# twizzley 

from base import Handler
from model import SellModel, FeedbackModel
from google.appengine.api import memcache
from helper import emailme
from ancestor import *


class FAQ(Handler):
    def get(self):
        count = memcache.get("TOTAL_TRANSACTED")

        if count is None:
            count = 0

            sells = SellModel.all().ancestor(sell_key())
            for item in sells:
                count += int(item.amount)

            memcache.set("TOTAL_TRANSACTED", count)

        self.render("faq.html", count=count)


class Feedback(Handler):
    def post(self):
        feedback = self.request.get('feedback')
        FeedbackModel(parent=feedback_key(), feedback=feedback).put()
        emailme(feedback)