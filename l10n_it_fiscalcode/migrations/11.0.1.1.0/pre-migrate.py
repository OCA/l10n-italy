# Copyright © 2018 Matteo Bilotta (Link IT s.r.l.)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    if not version:
        return

    cr.execute("DROP VIEW IF EXISTS res_city_it_code_province;")
