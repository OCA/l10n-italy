.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Pec Messages
============

This module extends the Odoo base email functionality support the
PEC standard (Italian Certified Email Communication) and correctly
correctly parse PEC messages (See images in docs for the message structure).
According to 'daticert.xml' file, it identifies the message type and other
message data.
'consegna', 'accettazione' and the other notification messages are linked to
the original message that originated them.
It also correctly parses the mail attachments and attaches the original 'eml'
PEC message.
The module adds a 'PEC' menu where to handle PEC messages.

https://it.wikipedia.org/wiki/Posta_elettronica_certificata

Installation
============

Nothing special is needed to install this module.

Configuration
=============

Create a New Alias from Settings/Technical/Email/Aliases menu
(
    Name of the alias = The username of the PEC mail,
    Alias Contact Security = Authenticated Partners,
    Aliased Model =	Users
)
Set 'Never' for 'Receive Messages by Email'.
Configure the fetchmail server (incoming mail server, IMAP or POP)
used to fetch PEC messages and set it as 'PEC'.
Set the users allowed to use that server.
Configure the 'outgoing mail server' (SMTP) used for PEC and set it as 'PEC'.
Link the outgoing mail server to the 'incoming PEC server'.
Add your user to 'PEC reader' group.


Known issues / Roadmap
======================

None known.


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/l10n-italy/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/l10n-italy/issues/new?body=module:%20l10n_it_pec_messages%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Alessio Gerace <alessio.gerace@gmail.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Roberto Onnis <roberto.onnis@innoviu.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
