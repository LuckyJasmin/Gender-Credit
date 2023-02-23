# -*- codeing = utf-8 -*-
# @Time: 2023/2/18 15:15
# @Author: Jasmin
# @File: tests.py.py
# @Software: PyCharm

from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        pass