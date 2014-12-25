pyMTGJSon
=========

A small python library designged to ease to write scripts/apps that use data
from `mtgjson.com <http://mtgjson.com>`_.

Example use
-----------

.. code:: python

   >>> from mtgjson import CardDb
   >>> db = CardDb.from_url()
   >>> card = db.find_card_by_name(u'aether vial')
   >>> card.name
   u'\xc6ther Vial'
   >>> print card.name
   Æther Vial
   >>> card.cmc
   1
   >>> card.text
   u'At the beginning of your upkeep, you may put a charge counter on \xc6ther Vial.\n{T}: You may put a creature card with converted mana cost equal to the number of charge counters on \xc6ther Vial from your hand onto the battlefield.'
   >>> card.img_url
   'http://mtgimage.com/set/MMA/aether vial.jpg'
