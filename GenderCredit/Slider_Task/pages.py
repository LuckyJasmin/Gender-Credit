# -*- codeing = utf-8 -*-
# @Time: 2023/2/17 12:09
# @Author: Jasmin
# @File: pages.py
# @Software: PyCharm

import time
from ._builtin import Page, WaitPage
from .models import Constants


class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.participant.vars['expiry'] = time.time() + 1.0 * 120
        self.group.set_slider_goals()


class StartRoundTwo(Page):
    def is_displayed(self):
        return self.round_number == 11

    def before_next_page(self):
        self.participant.vars['expiry'] = time.time() + 1.0 * 60


class Sliders(Page):
    form_model = 'player'
    form_fields = ['slider1']
    timer_text = 'Time left to complete the Sliders Task game:'


    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.get_timeout_seconds() > 3

    def vars_for_template(self):
        return dict(
            slider_goals_this_round=self.session.vars['slider_goals' + str(self.round_number)],
        )

    def before_next_page(self):
        self.group.check_slider_answers()

# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         self.group.check_slider_answers()


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return dict(
            player_in_all_rounds=self.player.in_all_rounds(),
            total_sliders_correct=sum([p.total_sliders_correct for p in self.player.in_all_rounds()]),
            total_payoff=sum([p.payoff for p in self.player.in_all_rounds()]),
        )


page_sequence = [
    Start,
    Sliders,
    # ResultsWaitPage,
    Results
]