# helper.py 
# emailme, process input
# twizzley 

import re
import math
import datetime
import random
from ancestor import *
from model import *
from string import letters
from google.appengine.api import mail
from google.appengine.api import memcache


def make_salt():
    salt = ''.join(random.choice(letters) for x in xrange(5))
    return salt

def emailme(message):
    sender = "bot@trademealpoints.appspotmail.com"
    receiver = "nj.fu@wustl.edu"
    subject = "tmp feedback"
    body = message
    mail.send_mail(sender, receiver, subject, body)




def commit_offer(user, amount, price, bool):
    offer = SellModel(parent=sell_key(),
                        user=user,
                        amount=amount,
                        price=price,
                        fulfilled=bool)
    offer.put()
    return offer

def make_code(email):
    code = make_salt()
    VerifyModel(parent=verify_key(),
                email=email,
                code=code).put()
    return code

def get_code(email): 
    # get "login code" for email link to see own posts
    v = VerifyModel.all().ancestor(verify_key()).filter("email", email).get()
    if not v:
        code = make_salt()
        v = VerifyModel(parent=verify_key(),
                    email=email,
                    code=code)
        v.put()
    return v.code




def update_cached_offers():
    memcache.delete("OFFERS")
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year

    if current_month < 9: # get last fall and current spring
        current_year -= 1

    offers = list(SellModel.all().ancestor(sell_key()).filter("fulfilled", False).filter("created >", datetime.datetime(current_year, 9, 1, 0, 0, 0)))

    if len(offers) != 0:
        memcache.set("OFFERS", offers.sort(key=lambda x: (float(x.price), int(x.amount))))

    return offers  # from current school year

def get_cached_offers():
    offers = memcache.get("OFFERS")
    if offers is None:  # nothing in memcache
        offers = update_cached_offers()
    else:  # render memcache
        offers.sort(key=lambda x: (float(x.price), int(x.amount)))
    return offers

def update_count(new_amount):
    #update total transacted count in memcache
    count = memcache.get("TOTAL_TRANSACTED")

    if count is None:
        count = 0
        sells = SellModel.all().ancestor(sell_key())
        for item in sells:
            count += int(item.amount)

    count += int(new_amount)
    memcache.set("TOTAL_TRANSACTED", count)




# filter
# else valid but ugly display
def prettyamount(amount):
    if not amount or amount.count('.') > 0: # eval to false
        return amount
    else: # no decimal: keep digits and lstrip
        return re.sub("[^0-9]", "", amount.lstrip('0'))

def prettyprice(price):
    if not price or price.count('.') > 1:  # eval to false
        return price

    else: # has decimal or just "1"
        price = price.strip('0').replace(" ", "").replace("$", "") # strip 0, space, $
        price = re.sub("[^0-9\.]", "", price) # keep only digits and decimals

        if len(price) == 1 and price.count('.') == 1: # just decimal
            return "0"
        else:  # should be okay here
            price = "{:3.2f}".format(float(price)) # fixed point num
            return price

def prettyemail(email):
    return email.lower()




# regex
def valid_amount(amount):
    return amount and re.compile(r'^[1][5-9][0-9]\.?$|^[2-9][0-9]{2}\.?$|^[1][0-9]{3}\.?$|^2000\.?$').match(amount)

def valid_price(price):
    return price and re.compile(r'^[0]?\.[0-9]*$|^1$|^1\.$|^1\.0*$').match(price)

def valid_email(email):
    return email and re.compile(r'^[\S]+(?i)(@wustl\.edu)$').match(email)

