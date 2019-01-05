pyMTGJSon
=========

A small python library designged to ease to write scripts/apps that use data
from `mtgjson.com <https://mtgjson.com>`_.

Example use
-----------

.. code:: python

    >>> from mtgjson import CardDb
    >>> db = CardDb.from_url()
    >>> card = db.cards_by_name['Aether Vial']
    >>> card.name
    'Aether Vial'
    >>> print(card.name)
    Aether Vial
    >>> card.convertedManaCost
    1
    >>> card.text
    'At the beginning of your upkeep, you may put a charge counter on Aether Vial.\n{T}: You may put a creature card with converted mana cost equal to the number of charge counters on Aether Vial from your hand onto the battlefield.'


See the documentation at http://pythonhosted.org/mtgjson for more.
