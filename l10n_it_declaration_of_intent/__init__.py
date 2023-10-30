#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import models
from . import wizard
from .hooks import pre_absorb_old_module
from .hooks import copy_m2m_values
