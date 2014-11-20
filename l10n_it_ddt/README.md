New DDT module
==============

This is a total refactoring of the previews module (l10n_it_sale v7).

With this brand new module we have the possibility to keep pickings and DdTs
separated.

The DdT is now a picking container, where the user can modify, remove and
insert new lines unrelated to the stock moves linked to the Ddt.

In the "Pickings" tab we can select the pickings related to the DdT and then we
press the "Update Lines" button.
This way the tab "DDT Lines" gets populated.
Here we can modify and rearrange the DDT lines (e.g. to group the lines by
client reference, to add descriptions, etc)

Nevertheless, we can select pickings and the use the "DdT from Pickings"
action to automatically create a DdT from the selected pickings and a new DdT
is automatically created after the confirmation of a sale order.
This DdT will contain all the pickings related to the confirmed sale order. 