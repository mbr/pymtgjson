import json
import os

from .jsonproxy import JSONProxy


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
    def __init__(self, db_file=None):
        if db_file is None:
            db_file = os.path.join(os.path.dirname(__file__), 'AllSets.json')

        self.db_file = db_file

        with open(self.db_file) as inp:
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
