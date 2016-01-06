# strings.py
# email messages

# .format(email, email, code)
link_message = """
                Hello! 
                \n
                This link highlights your offer on the buy page: \n
                trademealpoints.appspot.com/buy?e={}
                \n
                You can edit or remove your offers here: \n
                trademealpoints.appspot.com/change?e={}&v={}
                \n
                You can comment/ask for features/say hi here:\n
                trademealpoints.appspot.com/faq#feed
                \n
                Yours, 
                Bot
                """

seller_message = """
                Hey hey, savvy meal point seller. It looks like {} {} is interested in buying your offer of {} meal points at ${} per point!
                \n
                You can reach {} at {}. 
                \n
                To complete this transaction, arrange with {} to visit Dining Services Offices in the South Forth House to sign the transaction form. WashU takes a 15 point transaction fee, 7.5 points per person.
                \n
                If you have any questions/comments/just want to say hi,
                please leave them in the feedback box on the FAQ page!
                \n
                Mechanically yours,
                Bot 
                \n
                P.S. Your offer no longer appears on the 'buy' page. If you do not complete this transaction and want to re-list your offer, simply re-enter your info on the 'sell' page.
                """

buyer_message = """
                Hey hey, savvy meal point buyer. You can reach {} {} at {} regarding {}'s offer of {} meal points at ${} per point.
                \n
                To complete this transaction, arrange with {} to visit Dining Services Offices in the South Forth House to sign the transaction form. WashU takes a 15 point transaction fee, 7.5 points per person.
                \n
                If you have any questions/comments/just want to say hi,
                please leave them in the feedback box on the FAQ page!
                \n
                Mechanically yours,
                Bot
                \n
                P.S. Your offer no longer appears on the 'buy' page.
                If you do not complete this transaction and want to re-list your offer,
                simply re-enter your info on the 'sell' page.
                """
