# sell.py 
# process post input
# twizzley

from ancestor import *
from base import Handler
from helper import *
from model import *
from message import *


class Sell(Handler):

    def get(self):
        self.render("sell.html")

    def post(self):

        submit_button = self.request.get("submit_button")
        resend_button = self.request.get("resend_button")

        # post info
        amount = prettyamount(self.request.get('amount'))
        price = prettyprice(self.request.get('price'))
        email = prettyemail(self.request.get('email'))

        user = UserModel.all().ancestor(user_key()).filter("email", email).get()

        # user info. input boxes only show when
        # needs to register new user
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        code = self.request.get('code')

        # set up dict for page re-render
        params = dict(amount=amount,
                      price=price,
                      first_name=first_name,
                      last_name=last_name,
                      email=email)

        # submit new post
        if submit_button:

            # invalid input
            if not valid_amount(amount):
                params['stat'] = "150 to 2000 mp (whole numbers)"
                self.render("sell.html", **params)

            elif not valid_price(price):
                params['stat'] = "$0.01 to $1 per mp"
                self.render("sell.html", **params)

            elif not valid_email(email):
                params['stat'] = "Use your wustl email"
                self.render("sell.html", **params)

            # 3 valid inputs.
            elif not code:

                user = UserModel.all().ancestor(user_key()).filter("email", email).get()
                if user:  # commit offer for existing user
                    commit_offer(user, amount, price, False)
                    update_cached_offers()
                    update_count(int(amount))
                    code = get_code(email)

                    sender = "bot@trademealpoints.appspotmail.com"
                    receiver = email
                    subject = "Links for Selling Meal Points"
                    body = link_message.format(email, email, code)

                    mail.send_mail(sender, receiver, subject, body)
                    self.redirect('/buy?e=' + email)  # redirect to buy page with offer highlighted

                elif not user:  # no code nor usermodel, waiting to verify code or totally new user?
                    v = VerifyModel.all().ancestor(verify_key()).filter("email", email).get()

                    if v:  # sent email already, waiting to verify code
                        params['stat'] = "What is your verification code?"
                        params['need_code'] = True
                        self.render("sell.html", **params)

                    else:  # totally new user, send email with verification code
                        code = make_salt()
                        VerifyModel(parent=verify_key(),
                                    email=email,
                                    code=code).put()

                        sender = "bot@trademealpoints.appspotmail.com"
                        receiver = email
                        subject = "Verification code for selling meal points"
                        body = "Hello! Your verification code is " + code

                        mail.send_mail(sender, receiver, subject, body)
                        params['need_code'] = True
                        self.render("sell.html", **params)

            # 6 inputs.
            # new user trying to submit post
            # has verification code. check code
            elif first_name and last_name and code:
                v = VerifyModel.all().ancestor(verify_key()).filter("code", code).get()

                if v:  # everything okay
                    user = UserModel(parent=user_key(),
                              first_name=first_name,
                              last_name=last_name,
                              email=email)
                    user.put()

                    commit_offer(user, amount, price, False)
                    update_count(int(amount))
                    update_cached_offers()

                    sender = "bot@trademealpoints.appspotmail.com"
                    receiver = email
                    subject = "Links for editing meal point offer"
                    body = link_message.format(email, email, code)

                    mail.send_mail(sender, receiver, subject, body)
                    self.redirect("/buy?e=" + email)

                elif not v:  #OH SNAP. wrong code
                    params['stat'] = "Invalid code. Resend?"
                    params['need_code'] = True
                    self.render("sell.html", **params)

            else:  # missing first/last name
                params['stat'] = "Fill every box"
                self.render("sell.html", **params)

        elif resend_button:

            if not valid_email(email):
                params['stat'] = "Use your wustl email"
                self.render("sell.html", **params)

            else:
                code = get_code(email)

                sender = "bot@trademealpoints.appspotmail.com"
                receiver = email
                subject = "MEAL POINTS VERIFICATION"
                body = ("Hello! Your verification code is " + code)

                mail.send_mail(sender, receiver, subject, body)
                params['stat'] = "Code sent! Check your inbox"
                params['need_code'] = True
                self.render("sell.html", **params)
