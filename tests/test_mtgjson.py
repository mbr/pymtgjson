# coding: utf8

import os
import pytest
import requests

from mtgjson import CardDb, ALL_SETS_URL


def download_set_file(url, fn):
    tests_path = os.path.dirname(__file__)
    fn = os.path.join(tests_path, fn)

    if not os.path.exists(fn):
        resp = requests.get(url)
        resp.raise_for_status()

        with open(fn, 'wb') as out:
            out.write(resp.content)

    return fn


@pytest.fixture(scope='module',
                params=['url', 'file'])
def db(request):
    if request.param == 'url':
        return CardDb.from_url()
    elif request.param == 'file':
        return CardDb.from_file(
            download_set_file(ALL_SETS_URL, 'AllSets.json')
        )


def test_db_instantiation(db):
    pass


def test_get_card_by_name(db):
    card = db.cards_by_name['Sen Triplets']

    assert card.flavorText == 'They are the masters of your mind.'


def test_get_card_by_id(db):
    card = db.cards_by_id[180607]

    assert card.name == 'Sen Triplets'


def test_get_sen_triplets(db):
    card = db.cards_by_id[180607]

    assert card.name == 'Sen Triplets'
    assert card.manaCost == '{2}{W}{U}{B}'
    assert card.convertedManaCost == 5
    assert card.colors == ['B', 'U', 'W']
    assert card.type == u'Legendary Artifact Creature — Human Wizard'
    assert card.supertypes == ['Legendary']
    assert card.types == ['Artifact', 'Creature']
    assert card.subtypes == ['Human', 'Wizard']
    assert card.rarity == 'mythic'
    assert card.text == ('At the beginning of your upkeep, choose target '
                         'opponent. This turn, that player can\'t cast spells '
                         'or activate abilities and plays with their hand '
                         'revealed. You may play lands and cast spells from '
                         'that player\'s hand this turn.')
    assert card.flavorText == 'They are the masters of your mind.'
    assert card.artist == 'Greg Staples'
    assert card.number == '109'
    assert card.power == '3'
    assert card.toughness == '3'
    assert card.layout == 'normal'
    assert card.multiverseId == 180607
    assert card.ascii_name == 'sen triplets'


def test_set_list(db):
    # should start with alpha
    assert list(db.sets.values())[0].name == 'Limited Edition Alpha'
    assert len(db.sets) > 20


def test_cards_from_set(db):
    assert list(db.sets.values())[0].cards[0].name == 'Animate Wall'


def test_card_ascii_name(db):
    card = db.cards_by_id[23194]

    assert card.ascii_name == 'aether rift'


def test_cards_by_ascii_name(db):
    assert db.cards_by_ascii_name['aether rift'].name == u'Aether Rift'


def test_get_specific_card(db):
    assert db.sets['4ED'].cards_by_name['Lightning Bolt'].set.code == '4ED'


def test_different_sets_compare_nonequal(db):
    c1 = db.sets['4ED'].cards[-1]
    c2 = db.sets['ISD'].cards[0]

    assert c1 < c2


def test_urls(db):
    card = db.cards_by_id[23194]

    assert card.img_url == 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=23194&type=card'
    assert card.gatherer_url == 'https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=23194'