# buy.py 
# twizzley 

import logging
import datetime
from ancestor import *
from message import *
from model import *
from helper import *
from base import Handler
from google.appengine.api import memcache


class Buy(Handler):  # render current offers

    def get(self):
        offers = get_cached_offers()
        count = len(offers)
        email = self.request.get("e")
        self.render("buy.html", offers=offers, count=count, email=email)



class BuyContact(Handler):  # single post details

    def notify(self, amount, price, offer_id, buyer_email):
        offer = SellModel.get_by_id(int(offer_id), parent=sell_key())
        seller = offer.user
        buyer = UserModel.all().ancestor(user_key()).filter("email", buyer_email).get()
        sender = "bot@trademealpoints.appspotmail.com"

        # seller email
        subject = "Meal Point Buyer"
        receiver = seller.email
        body = seller_message.format(buyer.first_name, buyer.last_name, amount, price,
                       buyer.first_name, buyer_email,
                       buyer.first_name)
        mail.send_mail(sender, receiver, subject, body)

        # buyer email
        subject = "Buying Meal Points"
        receiver = buyer_email
        body = buyer_message.format(seller.first_name, seller.last_name, seller.email,
                           seller.first_name, amount, price,
                           seller.first_name)
        mail.send_mail(sender, receiver, subject, body)

        offer.fulfilled = True
        offer.put()

        update_cached_offers()

        stat = "check your inbox!"
        self.render("buycontact.html", stat=stat, amount=amount, price=price)

    def get(self):
        amount = self.request.get("amount")
        price = self.request.get("price")
        offer_id = self.request.get("id")

        if not amount or not price or not offer_id:
            self.redirect("/buy")
        else:
            self.render("buycontact.html", amount=amount, price=price)

    def post(self):
        offer_id = self.request.get("id")
        logging.error("ID: " + offer_id)

        submit_button = self.request.get("submit_button")
        resend_button = self.request.get("resend_button")
        code = self.request.get("code")

        amount = self.request.get("amount")
        price = self.request.get("price")

        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        buyer_email = self.request.get('email')

        params = dict(amount=amount,
                      price=price,
                      first_name=first_name,
                      last_name=last_name,
                      email=buyer_email)

        if submit_button:

            if valid_email(buyer_email):

                if code:

                    if first_name and last_name:
                        correct_code = VerifyModel.all().ancestor(verify_key()).filter("code", code).get()
                        if correct_code:
                            UserModel(parent=user_key(),
                                     first_name=first_name,
                                     last_name=last_name,
                                     email=buyer_email).put()
                            self.notify(amount, price, offer_id, buyer_email)

                        elif not correct_code:  
                            params['need_code'] = True
                            params['stat'] = "wrong code :|"
                            self.render("buycontact.html", **params)

                    elif not first_name or not last_name:
                        params['code'] = code
                        params['first_name'] = first_name
                        params['last_name'] = last_name

                        params['need_code'] = True
                        params['stat'] = "Fill every box"
                        self.render("buycontact.html", **params)

                else:  # didn't enter code
                    user = UserModel.all().ancestor(user_key()).filter("email", buyer_email).get()

                    if user: 
                        self.notify(amount, price, offer_id, buyer_email)

                    else:
                        waiting_for_verify = VerifyModel.all().ancestor(verify_key()).filter("email", buyer_email).get()
                        if not waiting_for_verify:  # gen code
                            code = make_code(buyer_email)
                            sender = "bot@trademealpoints.appspotmail.com"
                            receiver = buyer_email
                            subject = "Meal Points Verification Code"
                            body = ("Hello! Your verification code is" + code)
                            mail.send_mail(sender, receiver, subject, body)

                        params['need_code'] = True
                        self.render("buycontact.html", **params)  #ask for code either way                        

            elif not valid_email(buyer_email):
                if first_name and last_name:
                    params['need_code'] = True
                params['stat'] = "Use your wustl email"
                self.render("buycontact.html", **params)

        elif resend_button:
            if valid_email(buyer_email):
                code = get_code(buyer_email)

                sender = "bot@trademealpoints.appspotmail.com"
                receiver = buyer_email
                subject = "MEAL POINTS VERIFICATION"
                body = "Hello! Your verification code is " + code

                mail.send_mail(sender, receiver, subject, body)
                params['need_code'] = True
                self.render("buycontact.html", **params) 

            else:
                params['need_code'] = True
                params['stat'] = "Use your wustl email"
                self.render("buycontact.html", **params)
