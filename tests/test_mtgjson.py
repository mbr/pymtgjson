# coding: utf8

import pytest

from mtgjson import CardDb


@pytest.fixture(scope='module',
                params=['url', 'file'])
def db(request):
    if request.param == 'url':
        return CardDb.from_url()
    elif request.param == 'file':
        return CardDb.from_file()


def test_db_instantiation(db):
    pass


def test_get_card_by_name(db):
    card = db.get_card_by_name('Sen Triplets')

    assert card.multiverseid == 180607


def test_get_card_by_id(db):
    card = db.get_card_by_id(180607)

    assert card.name == 'Sen Triplets'


def test_get_sen_triplets(db):
    card = db.get_card_by_id(180607)

    assert card.name == 'Sen Triplets'
    assert card.manaCost == '{2}{W}{U}{B}'
    assert card.cmc == 5
    assert card.colors == ['White', 'Blue', 'Black']
    assert card.type == u'Legendary Artifact Creature — Human Wizard'
    assert card.supertypes == ['Legendary']
    assert card.types == ['Artifact', 'Creature']
    assert card.subtypes == ['Human', 'Wizard']
    assert card.rarity == 'Mythic Rare'
    assert card.text == ('At the beginning of your upkeep, choose target '
                         'opponent. This turn, that player can\'t cast spells '
                         'or activate abilities and plays with his or her hand'
                         ' revealed. You may play cards from that player\'s '
                         'hand this turn.')
    assert card.flavor == 'They are the masters of your mind.'
    assert card.artist == 'Greg Staples'
    assert card.number == '109'
    assert card.power == '3'
    assert card.toughness == '3'
    assert card.layout == 'normal'
    assert card.multiverseid == 180607
    assert card.imageName == 'sen triplets'
