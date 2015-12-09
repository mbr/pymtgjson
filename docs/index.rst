.. include:: ../README.rst

The database object
-------------------

Since the actual data files are not included, they either need to be supplied
or downloaded upon instantiation. Redownloading them every time the application
is started is usually a bad idea, but may be feasible if you expect restarts on
every few days.

The quickest way to get started is::

  from mtgjson import CardDb
  db = CardDb.from_url()

This will download ``AllSets.json`` from the http://mtgjson.com website. You
can pass in a different address as well::

  db = CardDb.from_url(ALL_SETS_X_ZIP_URL)

Here ``ALL_SETS_X_ZIP_URL`` is one of the constants that hold the URLs for
http://mtgjson.com download links.

If you've downloaded the files already, the :func:`~mtgjson.CardDb.from_file`
function allows you to pass these files to the :class:`~mtgjson.CardDb`.

If your data is stored elsewhere, it is always possible to just pass the data
dictionary (i.e. the output of :func:`~json.loads`) directly to
:class:`~mtgjson.CardDb`.

.. autoclass:: mtgjson.CardDb
   :members:

   .. attribute:: cards_by_id

      Contains a mapping of card numbers (the multiverse id) to
      :class:`~mtgjson.CardProxy` instances. Should be used to look up card by
      their IDs::

          card = db.cards_by_id[180607]

      Note that the multiverse id (like the name) does not specificy which set
      a card is from if it has been reprinted. The returned card will always be
      the most recent printing.

   .. attribute:: cards_by_name

      Like ``mtgjson.CardProxy.cards_by_id``, but indexed by card name::

          card = db.cards_by_name['Sen Triplets']

   .. attribute:: cards_by_ascii_name

      Uses a lower-case, ascii-only version of the card name::

          card = db.cards_by_ascii_name['jotun grunt']
          assert card.name == u'Jötun Grunt'

   .. attribute:: sets

      An :class:`~collections.OrderedDict` of all sets found in the data file.
      Keys are the three-letter set codes (like ``ISD`` for Inistrad), mapped
      onto :class:`~mtgjson.SetProxy` instances. Ordered by publishing date,
      i.e. Limited Edition Alpha is the first value of the dict.


Cards
-----

Cards retrieved are usually :class:`~mtgjson.CardProxy` instances:

.. autoclass:: mtgjson.CardProxy
   :members:


Sets
----

Sets, similar to cards are wrapped in :class:`~mtgjson.SetProxy`:

.. autoclass:: mtgjson.SetProxy
   :members:

   .. attribute:: cards_by_id

      Similar to ``mtgjson.CardDb.cards_by_id``, but will always point to
      the card instance of this specific set instead of the latest.

   .. attribute:: cards_by_name

      See above.

This is especially important when trying to fetch a card of a specific set::

   # get an unlimited black lotus
   card = db.cards_by_name('Black Lotus')

   # black bordered, please:
   beta = db.sets['LEB']
   card = beta.cards_by_name('Black Lotus')
