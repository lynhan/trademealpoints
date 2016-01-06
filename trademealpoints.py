# main.py 
# set up routes
# twizzley 

import os
import logging
from webapp2 import WSGIApplication, Route
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

root_dir = os.path.dirname(__file__)
template_dir = os.path.join(root_dir, 'html')

# handle inbound mail
class LogSenderHandler(InboundMailHandler):

    def receive(self, mail_message):
        logging.info("from: " + mail_message.sender)
        plaintext = mail_message.bodies(content_type='text/plain')
        for text in plaintext:
            m = ""
            m = text[1].decode()
            logging.info("message: %s" % m)
            self.response.out.write(m)


# create the WSGI application and define route handlers
# use route objects instead of tuples like ('/', Buy)

app = WSGIApplication([

        Route(r'/', handler = "python.buy.Buy", name = "buy"),
        Route(r'/buy', handler = "python.buy.Buy", name = "buy"),
        Route(r'/contact', handler = "python.buy.BuyContact", name = "buycontact"),

        Route(r'/sell', handler = "python.sell.Sell", name = "sell"),
        Route(r'/changeoffer', handler = "python.edit.Edit", name = "edit"),
        Route(r'/change', handler = "python.edit.EditFinish", name = "editfinish"),

        Route(r'/delete', handler = "python.delete.DeleteOffer", name = "delete"),
        Route(r'/faq', handler = "python.faq.FAQ", name = "faq"),

        Route(r'/submitfeed', handler = "python.faq.Feedback", name = "submitfeed"),
        Route(r'/getkarma', handler = "python.money.PayMe", name = "money"),

        LogSenderHandler.mapping()],
        debug=True)
