import json
import os

import requests

from .jsonproxy import JSONProxy


ALL_SETS_URL = 'http://mtgjson.com/json/AllSets.json'
ALL_SETS_X_URL = 'http://mtgjson.com/json/AllSets-x.json'


class CardProxy(JSONProxy):
    @property
    def img_url(self):
        return 'http://mtgimage.com/set/{}/{}.jpg'.format(
            self.set.code, self.name,
        )

    @property
    def gatherer_url(self):
        return ('http://gatherer.wizards.com/Pages/Card/'
                'Details.aspx?multiverseid={}').format(self.multiverseid)


class CardDb(object):
    def __init__(self, db_file=None, db_url=None):
        if db_file is not None and db_url is not None:
            raise RuntimeError('Cannot use both db_file and db_url')

        # default is using the bundled file
        if db_file is None and db_url is None:
            db_file = os.path.join(os.path.dirname(__file__), 'AllSets.json')

        if db_url is not None:
            r = requests.get(db_url)
            r.raise_for_status()
            self._card_db = json.loads(r.text)
        elif db_file is not None:
            with open(db_file) as inp:
                self._card_db = json.load(inp)

        self._id_map = {}
        self._name_map = {}

        # sort sets by release date
        sets = sorted(self._card_db.itervalues(),
                      key=lambda s: s['releaseDate'])
        for _set in sets:
            set = JSONProxy(_set)
            set_cards = []
            for c in set.cards:
                card = CardProxy(c)

                self._name_map[card.name] = card
                if not hasattr(card, 'multiverseid'):
                    continue

                self._id_map[card.multiverseid] = card
                card.set = set

                set_cards.append(card)
            set.cards = set_cards

    def get_card_by_id(self, id):
        return self._id_map[id]

    def get_card_by_name(self, name):
        return self._name_map[name]
