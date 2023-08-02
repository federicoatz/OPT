
from otree.api import *
c = cu

doc = ''
class C(BaseConstants):
    NAME_IN_URL = 'Optimism_Task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_CARDS = 21
    DECK_SIZE = 52
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    from random import shuffle
    if subsession.round_number == 1:
        deck = list(range(1, C.DECK_SIZE + 1))
    shuffle(deck)
    session.vars['deck'] = deck
class Group(BaseGroup):
    pass
class Player(BasePlayer):
    chosen_card = models.IntegerField(label='Choose a card (1 to 21) from the deck:', max=C.NUM_CARDS, min=1)
    chosen_color = models.StringField()
    same_color_cards = models.IntegerField()
    guess_n_cards = models.IntegerField(label='Now, try to guess the number of cards in your sample reporting the same color', max=21, min=0)
def set_payoff(player: Player):
    session = player.session
    participant = player.participant
    deck = player.session.vars['deck']
    
    chosen_card_color = 'red' if player.chosen_card % 2 == 1 else 'black'
    
    same_color_cards = sum(1 for card in deck[:C.NUM_CARDS] if card % 2 == player.chosen_card % 2)
    
    player.same_color_cards = same_color_cards
    
    player.chosen_color = chosen_card_color
    
    if same_color_cards == player.guess_n_cards:
        winnings = (sum(1 for card in deck[:C.NUM_CARDS] if card % 2 == player.chosen_card % 2)) + (10)
    else:
        winnings = same_color_cards
    
    participant.opt_payoff=winnings
class Instructions(Page):
    form_model = 'player'
class SelectCard(Page):
    form_model = 'player'
    form_fields = ['chosen_card']
    @staticmethod
    def vars_for_template(player: Player):
        return {
                    'deck_size': C.DECK_SIZE
                }
class Guess(Page):
    form_model = 'player'
    form_fields = ['guess_n_cards']
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoff(player)
class ResultsPage(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        return {
                    'winnings': player.payoff,
                    'num_cards': C.NUM_CARDS,
                    'chosen_color': player.chosen_color,
                    'same_color_cards': str(player.same_color_cards),
                    'guessed_cards':player.guess_n_cards
                }
        
page_sequence = [Instructions, SelectCard, Guess, ResultsPage]