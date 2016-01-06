# buy.py 
# twizzley 

import re
import logging
import stripe
from base import Handler
from config import stripe_private_key

class PayMe(Handler):

    def valid_amount(self, payment):
        if payment.count('.') > 1 or len(payment) == 0:
            return False

        else:  # has . or none
            if len(payment) == 1 and payment.count('.') == 1:  #entry is just .
                return False

            elif payment.count('.') == 1:
                payment = payment.strip('0')
                return payment and re.compile(r'^[0-9]?\.[0-9]*$').match(payment)

            elif payment.count('.') == 0:
                return payment and re.compile(r'^[0-9]+$').match(payment)

    def get(self):
        self.render("payme.html")

    def post(self):
        stripe.api_key = stripe_private_key  #https://manage.stripe.com/account/apikeys

        token = self.request.get('stripeToken')
        email = self.request.get('email')
        amount = self.request.get('amount')
        error = False

        params = dict(amount=amount, email=email)

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            error = True
            params['emailstat'] = "Please enter a valid email"

        if not self.valid_amount(amount):
            error = True
            params['amountstat'] = "Please enter a valid amount"

        elif self.valid_amount(amount):
            amount = float(amount)
            if amount < 1:
                error = True
                params['amountstat'] = "Coffee costs at least $1"

        if error:
            self.render("payme.html", **params)

        else:
            try:
                customer = stripe.Customer.create(
                    card=token,
                    email=email
                )
                amount = int(amount)
                charge = stripe.Charge.create(
                    customer=customer.id,
                    amount=amount * 1000,  #cents
                    currency="usd"
                )

                logging.error("amount " + str(amount * 1000))

                self.render("payme.html", woohoo=True)

            except stripe.CardError, e:
                params['stat'] = "Your card was declined."
                self.render("payme.html", **params)
                