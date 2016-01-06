# cron.py 
# twizzley 

from base import Handler
from model import *
from ancestor import *
from google.appengine.api import mail


class UnsoldReminder(Handler):
    def post(self):
        pass
        # unsold = SellModel.all().ancestor(sell_key()).filter('fulfilled', False)
        
        # # remind poster to edit
        # for offer in unsold:

        #     v = VerifyModel.all().ancestor(verify_key()).filter('email', offer.user.email).get()
        #     sender = "bot@trademealpoints.appspotmail.com"
        #     receiver = offer.user.email
        #     subject = "FRIENDLY MEAL POINT REMINDER"
        #     body = (
        #         """
        #         Hello! It looks like your meal points are still on the market.
        #         You can check out your (highlighted) offer here: \n

        #         trademealpoints.appspot.com/buy?e={}

        #         \n\n

        #         If you would like to edit your offer, here is a link for that: \n

        #         trademealpoints.appspot.com/change?e={}&v={}

        #         \n\n

        #         (It usually helps to price your offer around the current lowest market price.)

        #         \n\n

        #         If you have any questions, please write them here: \n

        #         trademealpoints.appspot.com/faq#feed

        #         \n\n

        #         Thanks for using Trade Meal Points! You can share this web app with this link: \n
        #         http://trademealpoints.appspot.com

        #         \n\n

        #         Have an A1 day!\n

        #         Bot
        #         """.format(offer.user.email, offer.user.email, v.code)
        #     )
        #     mail.send_mail(sender, receiver, subject, body)
