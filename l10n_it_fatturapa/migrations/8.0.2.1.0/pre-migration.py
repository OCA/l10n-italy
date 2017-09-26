# -*- coding: utf-8 -*-
# Copyright 2017 Lorenzo Battistini - Agile Business Group


def migrate(cr, version):
    cr.execute(
        "UPDATE account_tax t SET kind_id = "
        "(SELECT id FROM account_tax_kind k "
        "WHERE k.code = t.non_taxable_nature)")
