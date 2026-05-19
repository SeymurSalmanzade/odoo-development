# -*- coding: utf-8 -*-

from . import models
from . import wizard

def post_init_hook(env):
    """
    Fetches all the sale order and resets the sequence of the order lines
    """
    sale = env['sale.order'].search([])
    sale._reset_sequence()