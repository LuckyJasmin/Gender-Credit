# -*- codeing = utf-8 -*-
# @Time: 2023/2/18 15:15
# @Author: Jasmin
# @File: pages.py.py
# @Software: PyCharm

import time

from ._builtin import Page, WaitPage
from .models import Constants


class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 2 minutes to complete as many pages as possible
        self.participant.vars['expiry'] = time.time() + 120

class zeroCount(Page):
    form_model = 'player'
    form_fields = ['count']

    timer_text = 'Time left to complete the Counting Zeros game:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.get_timeout_seconds() > 3

    def vars_for_template(self):
        return dict(
            #image_path='images/{}.PNG'.format(self.round_number)
            image_path='counting_zeros_task/{}.PNG'.format(self.round_number)

        )

    def before_next_page(self):
        self.group.check_count()
        self.group.count_correct_rounds()

# class ResultsWaitPage(WaitPage):
#     def get_timeout_seconds(self):
#         return self.participant.vars['expiry'] - time.time()
#
#     def is_displayed(self):
#         return self.get_timeout_seconds() > 5
#
#     def after_all_players_arrive(self):
#
#         self.group.check_count()
#         self.group.count_correct_rounds()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            number_of_rounds_played=self.round_number,
            rounds_correct=self.player.total_rounds_correct,
            total_payoff=sum([p.payoff for p in self.player.in_all_rounds()]),
            player_in_all_rounds=self.player.in_all_rounds(),
        )


page_sequence = [
    Start,
    zeroCount,
    Results,
]
