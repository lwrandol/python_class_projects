#!/usr/bin/env python

import random
from IPython.display import clear_output

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#Creates each individual card
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


    def __str__(self):
        return self.rank + ' of ' + self.suit

#Creates a full deck of cards
class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        complete_deck = ''
        for card in self.deck:
            complete_deck += '\n' + card.__str__()
        return 'The deck is: '+ complete_deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

#Creates a hand of two cards for each player
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

#Creates a stack of chips for each player
class Chips:

    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

#Asked the player to input a bet amount for each hand.
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('Enter a bet amount: '))

        except ValueError:
            print("I'm sorry. Please enter an integer.")

        else:
            if chips.bet > chips.total:
                print('Sorry. Your bet cannot exceed', chips.total)
            else:
                break

#Gives the player/dealer a single card when called
def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

#Askes player if they want to take another card to stand with the hand they currently have
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop

    while True:
        choice = input('\nWould you like to hit or stand? Enter "H" or "S" to choose. ').upper()

        if choice[0] == 'H':
            hit(deck, hand)

        elif choice[0] == 'S':
            print('Player stands. Dealer is playing...')
            playing = False

        else:
            print("\nI'm sorry. I did not understand your selection. Please try again")
            continue
        break

#Displays the players entire hand and hides one of the dealers two cards until dealers turn.
def show_some(player,dealer):

    clear_output()
    print('\nPlayer Hand:')
    for card in player.cards:
        print(card)
    print(f'Total: {player.value}')

    print('\nDealer Hand:')
    print(f'{dealer.cards[1]}')
    print('XXXXXXXXXXXXXX')

#Shows all cards from both hands.
def show_all(player,dealer):

    clear_output()
    print('\nPlayer Hand:')
    for card in player.cards:
        print(card)

    print(f'Total: {player.value}')

    print('\nDealer Hand:')
    for card in dealer.cards:
        print(card)
    print(f'Total: {dealer.value}')

#Dealer wins function if player hand valuevexceeds 21
def player_busts(player_chips, dealer_chips):
    print('\nPlayer Busted!')
    player_chips.lose_bet()
    dealer_chips.win_bet()

#Player wins function if players hand value is higher than dealers but also below 21
def player_wins(player_chips, dealer_chips):
    print('\nPlayer Wins!')
    player_chips.win_bet()
    dealer_chips.lose_bet()

#Player wins function if dealer hand value exceeds 21
def dealer_busts(player_chips, dealer_chips):
    print('\nDealer Busted!')
    dealer_chips.lose_bet()
    player_chips.win_bet()

#Dealer win fuction if dealer hand value is higher than players but also below 21
def dealer_wins(player_chips, dealer_chips):
    print('\nDealer Wins!')
    dealer_chips.win_bet()
    player_chips.lose_bet()

#Tie function
def push():
    print('\nPlayer and Dealer Tie! It is a push!')

# Set up the Player's chips
player_chips = Chips()

dealer_chips = Chips()

while True:
# Print an opening statement
    print('\nWelcome to Black Jack!')
    player = True

    # Create & shuffle the deck, deal two cards to each player
    game_deck = Deck()
    game_deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(game_deck.deal())
    player_hand.add_card(game_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(game_deck.deal())
    dealer_hand.add_card(game_deck.deal())

    # Prompt the Player for their bet
    take_bet(player_chips)
    dealer_chips.bet = player_chips.bet

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function

        # Prompt for Player to Hit or Stand
        hit_or_stand(game_deck, player_hand)

        # Show cards (but keeps one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, runs player_busts() and breaks out of loop
        if player_hand.value > 21:
            player_busts(player_chips, dealer_chips)
            break

    # If Player hasn't busted, plays Dealer's hand until Dealer reaches 17 higher
    if player_hand.value <= 21:

        while dealer_hand.value <= 17:
            hit(game_deck, dealer_hand)

        # Show all cards once its the dealers turn
        show_all(player_hand, dealer_hand)

        # Running different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_chips, dealer_chips)

        elif player_hand.value > dealer_hand.value:
            player_wins(player_chips, dealer_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips, dealer_chips)

        else:
            push()

    # Informs Player of their chips total
    print('Player, your chip total is ', player_chips.total)
    print("The Dealer's chip total is", dealer_chips.total)


    #Game winner check

    if player_chips.total <= 0:
        print('-------------------------------')
        print("\nI'm sorry, you are out of chips. You have lost")
        break

    elif dealer_chips.total <= 0:
        print('-------------------------------')
        print('The dealer is out of chips! Congrats you win!')
        break
    else:
        continue

    # Ask to play again
    play_again = input('\nWould you like to play another hand? Y or N ').upper()

    if play_again[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break
