# edit.py 
# twizzley 

import logging
from ancestor import *
from base import Handler
from helper import *
from message import *
from model import *
from google.appengine.api import memcache


class Edit(Handler):  # enter email, get links
    def get(self):
        self.render("edit.html")

    def post(self):
        email = self.request.get("email")
        if valid_email(email):
            user = UserModel.all().ancestor(user_key()).filter("email", email).get()
            offer = SellModel.all().ancestor(sell_key()).filter("user", user).get()
            if offer:
                code = get_code(email)
                sender = "bot@trademealpoints.appspotmail.com"
                receiver = email
                subject = "Links for editing meal point offer"

                body = link_message.format(email, email, code)
                mail.send_mail(sender, receiver, subject, body)
                self.render("edit.html", stat='Check your email!')
            else:
                stat = "You don't have any offers on the market."
                self.render("edit.html", stat=stat)
        else:
            stat = "(You used your wustl email)"
            self.render("edit.html", stat=stat)


class EditFinish(Handler):  # edit personal offers
    def get(self):
        email = self.request.get('e')
        code = self.request.get('v')
        okaycode = VerifyModel.all().ancestor(verify_key()).filter('email', email).filter('code', code).get()

        if okaycode:
            user = UserModel.all().ancestor(user_key()).filter("email", email).get()
            offer = list(SellModel.all().ancestor(sell_key()).filter('user', user).filter('fulfilled', False))
            offer.sort(key=lambda x: ((float)(x.amount), (float)(x.price)))
            self.render("editfinish.html", offer=offer)

        else:
            self.redirect('/changeoffer')

    def post(self):

        edit_button = self.request.get('edit_button')
        email = self.request.get("e")
        user = UserModel.all().filter("email", email).get()
        offer = list(SellModel.all().ancestor(sell_key()).filter('user', user).filter('fulfilled', False).order('amount'))
        offer.sort(key=lambda x: (float(x.amount), float(x.price)))

        if edit_button:
            amount = self.request.get_all("amount")
            price = self.request.get_all("price")

            if len(offer) == len(amount) and len(offer) == len(price):  # no blank fields
                change = False
                wrongamount = False
                wrongprice = False

                for x in range(0, len(offer)):
                    if prettyamount(offer[x].amount) != prettyamount(amount[x]):
                        change = True
                        if valid_amount(prettyamount(amount[x])):
                            offer[x].amount = prettyamount(amount[x])
                            offer[x].put()
                        else:
                            wrongamount = True

                    if prettyprice(offer[x].price) != prettyprice(price[x]):
                        change = True
                        if valid_price(prettyprice(price[x])):
                            offer[x].price = prettyprice(price[x])
                            offer[x].put()
                        else:
                            wrongprice = True

                if change:
                    offer = list(SellModel.all().ancestor(sell_key()).filter('user', user).filter('fulfilled', False).order('amount'))
                    offer.sort(key=lambda x: ((float)(x.amount), (float)(x.price)))

                    if wrongamount:  
                        self.render("editfinish.html", offer=offer,
                                    editstat="Wow. Such typing. Make sure your offer is between 150 and 2000 mp")
                    elif wrongprice:
                        self.render("editfinish.html", offer=offer, editstat="0.01 to 1.00 per mp")

                    else:  # everything okay
                        update_cached_offers()
                        self.render("editfinish.html", offer=offer, editstat="Updated successfully!")

                elif not change:
                    logging.error("NO CHANGE")
                    self.render("editfinish.html", offer=offer, editstat="Updated successfully!")

            else:  # blank field
                self.render("editfinish.html", offer=offer, editstat="Fill each box")
