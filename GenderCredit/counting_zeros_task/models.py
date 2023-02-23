from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)



#to be solved: 1)the summary page: correct number are wrong; 2)the image can not be shown


doc = """Player will be given a paragraph of ones and zeros.  The player will count the number of zeros in the 
paragraph as quickly and accurately as they can and type their answer.  The player will be rewarded for every 
paragraph that they count correctly. """


class Constants(BaseConstants):
    name_in_url = 'counting_zeros_task'
    players_per_group = None
    num_rounds = 10
    STATIC_URL = "/static/"

class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["correct_count_key"] = [7, 8, 9,10,9,11,7,6,8,8]

class Group(BaseGroup):
    def check_count(self):
        counter = self.get_player_by_role('Counter')

        for p in self.get_players(): #what is p here?
                    if counter.count == self.session.vars["correct_count_key"][self.round_number - 1]:
                        counter.is_winner = True
                        counter.payoff = c(10)

                    else:
                        counter.is_winner = False
                        counter.payoff = c(0)




    def count_correct_rounds(self):
        counter = self.get_player_by_role('Counter')
        if self.round_number == 1:
            if counter.is_winner:
                counter.total_rounds_correct = 1
        if self.round_number != 1:
            if counter.is_winner:
                counter.total_rounds_correct = counter.in_round(self.round_number - 1).total_rounds_correct + 1
            else:
                counter.total_rounds_correct = counter.in_round(self.round_number - 1).total_rounds_correct



class Player(BasePlayer):
    count = models.IntegerField(min=0, label="How many zeros are in the table?")

    is_winner = models.BooleanField()
    # payoff = models.CurrencyField()

    total_rounds_correct = models.IntegerField(initial=0)
    current_round_correct_answer = models.IntegerField(initial=0)

    def role(self):
        if self.id_in_group == 1:
            return 'Counter'