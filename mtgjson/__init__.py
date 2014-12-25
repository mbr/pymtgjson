try:
    from six.moves import cStringIO as StringIO
except ImportError:
    from six import StringIO as StringIO
import json
import os
import zipfile

import requests

from .jsonproxy import JSONProxy


ALL_SETS_URL = 'http://mtgjson.com/json/AllSets.json.zip'
ALL_SETS_X_URL = 'http://mtgjson.com/json/AllSets-x.json.zip'

ALL_SETS_PATH = os.path.join(os.path.dirname(__file__), 'AllSets.json')


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
    def __init__(self, db_dict):
        self._card_db = db_dict

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

    @classmethod
    def from_file(cls, db_file=ALL_SETS_PATH):
        if callable(getattr(db_file, 'read', None)):
            return cls(json.load(db_file))
        with open(db_file) as inp:
            return cls(json.load(inp))

    @classmethod
    def from_url(cls, db_url=ALL_SETS_URL):
        r = requests.get(db_url)
        r.raise_for_status()

        if r.headers['content-type'] == 'application/json':
            return cls(json.loads(r.content))

        if r.headers['content-type'] == 'application/zip':
            with zipfile.ZipFile(StringIO(r.content), 'r') as zf:
                names = zf.namelist()
                assert len(names) == 1, 'One datafile in ZIP'
                return cls.from_file(zf.open(names[0]))

    def get_card_by_id(self, id):
        return self._id_map[id]

    def get_card_by_name(self, name):
        return self._name_map[name]
