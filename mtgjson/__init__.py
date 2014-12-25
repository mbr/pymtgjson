try:
    from six.moves import cStringIO as StringIO
except ImportError:
    from six import StringIO as StringIO
from collections import OrderedDict
from functools import total_ordering
import json
from operator import itemgetter
import os
import re
import zipfile

import requests
from unidecode import unidecode

from .jsonproxy import JSONProxy


ALL_SETS_URL = 'http://mtgjson.com/json/AllSets.json'
ALL_SETS_X_URL = 'http://mtgjson.com/json/AllSets-x.json'

ALL_SETS_ZIP_URL = ALL_SETS_URL + '.zip'
ALL_SETS_X_ZIP_URL = ALL_SETS_X_URL + '.zip'

ALL_SETS_PATH = os.path.join(os.path.dirname(__file__), 'AllSets.json')


_WS = re.compile('\s+')


def to_find_name(name):
    return _WS.sub(' ', unidecode(name)).strip().lower()


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

    @property
    def ascii_name(self):
        return unidecode(self.name)

    @property
    def find_name(self):
        return to_find_name(self.name)


class SearchMixin(object):
    def find_card_by_name(self, fname):
        return self.cards_by_fname[to_find_name(fname)]


class SetProxy(JSONProxy, SearchMixin):
    def __init__(self, data):
        super(SetProxy, self).__init__(data)
        self.cards_by_name = {}
        self.cards_by_fname = {}

        cards = []
        for c in self.cards:
            card = CardProxy(c)
            card.set = self

            self.cards_by_name[card.name] = card
            self.cards_by_fname[card.find_name] = card
            cards.append(card)

        self.cards = sorted(cards)


@total_ordering
class CardDb(SearchMixin):
    def __init__(self, db_dict):
        self._card_db = db_dict

        self.cards_by_id = {}
        self.cards_by_name = {}
        self.cards_by_fname = {}
        self.sets = OrderedDict()

        # sort sets by release date
        sets = sorted(self._card_db.itervalues(),
                      key=itemgetter('releaseDate'))
        for _set in sets:
            s = SetProxy(_set)
            self.sets[s.code] = s

            self.cards_by_name.update(s.cards_by_name)
            self.cards_by_fname.update(s.cards_by_fname)
            for card in s.cards:
                if not hasattr(card, 'multiverseid'):
                    continue

                self.cards_by_id[card.multiverseid] = card

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        try:
            mynum = int(getattr(self, 'number', None))
            othernum = int(getattr(other, 'number', None))
            return mynum < othernum
        except TypeError:
            pass  # not comparable, no valid integer number

        # try creating a pseudo collectors number
        def _getcol(c):
            if hasattr(c, 'colors'):
                if len(c.colors) > 1:
                    return 'Gold'
                return c.colors[0]
            else:
                if 'Land' in c.types:
                    return 'Land'
                else:
                    return 'Artifact'

        col_order = ['White', 'Blue', 'Black', 'Red', 'Green', 'Gold',
                     'Artifact', 'Land']

        if col_order.index(_getcol(self)) < col_order.index(_getcol(other)):
            return True

        # go by name
        return self.name < other.name

    @classmethod
    def from_file(cls, db_file=ALL_SETS_PATH):
        if callable(getattr(db_file, 'read', None)):
            return cls(json.load(db_file))
        with open(db_file) as inp:
            return cls(json.load(inp))

    @classmethod
    def from_url(cls, db_url=ALL_SETS_ZIP_URL):
        r = requests.get(db_url)
        r.raise_for_status()

        if r.headers['content-type'] == 'application/json':
            return cls(json.loads(r.content))

        if r.headers['content-type'] == 'application/zip':
            with zipfile.ZipFile(StringIO(r.content), 'r') as zf:
                names = zf.namelist()
                assert len(names) == 1, 'One datafile in ZIP'
                return cls.from_file(zf.open(names[0]))
