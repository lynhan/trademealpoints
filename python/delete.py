# delete.py 
# twizzley 

from ancestor import *
from base import Handler
from helper import *
from model import *


class DeleteOffer(Handler):

    def post(self):
        email = self.request.get('email')
        amount = self.request.get('amount')
        price = self.request.get('price')

        user = UserModel.all().ancestor(user_key()).filter('email', email).get()
        offer = SellModel.all().ancestor(sell_key()).filter('user', user).filter('fulfilled', False).filter('amount', amount).filter('price',price).get()
        offer.delete()
        update_cached_offers()
