from flask import Flask
from flask_ask import Ask, statement, session, question
import logging
import os
import random

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger('flask_ask').setLevel(logging.DEBUG)
choices = ["rock", "scissors", "paper"]

win_states = {
    'rock':'scissors',
    'scissors': 'paper',
    'paper': 'rock',
}


def score():
    return "You {},  Alexa {}. ".format(sum([1 for x in session.attributes["Score"] if x[2]==1]),
                                     sum([1 for x in session.attributes["Score"] if x[2] == -1]))


def who_win(player, alexa):
    if player == alexa:
        add_score((player, alexa, 0,))
        return "My choice is {}, No one wins.".format(alexa)
    if win_states[player] == alexa:
        add_score((player, alexa, 1,))
        return "My choice is {}, you win because {} beats {}!".format(alexa, player, alexa)
    add_score((player, alexa, -1,))
    return "My choice is {}, I win because {} beats {}!".format(alexa, alexa, player)


def add_score(score):
    if "Score" not in session.attributes:
        session.attributes["Score"] = []
    session.attributes["Score"].append(score)

@ask.intent('StartGame')
def start():
        txt = "Let's play! I have already chosen, what is your choice?"
        return question(txt).simple_card('game', txt)


@ask.intent('PlayerChoice', mapping={'player_choice': 'Choice'})
def choice(player_choice):
    try:
        alexa_choice = random.choice(choices)
        txt = who_win(player_choice,alexa_choice)  + ". Do you want to play again?"
    except Exception, e:
        txt = "Sorry but I do not understand, please repeat"
    return question(txt).simple_card('game', txt)


@ask.launch
def launch():
    txt = "Welcome to rock paper scissors demo game. Do you want to play?"
    return question(txt).simple_card('start game', txt)


def game_history():
    if "Score" not in session.attributes:
        session.attributes["Score"] = []
    return "You have won {} times".format(sum([1 for x in session.attributes["Score"] if x[2]==1]))


@ask.intent('PlayerScore')
def player_score(player_choice):
        txt = game_history()
        return question(txt)

@ask.intent('EndGame')
def end():
        txt = "{} {}".format(" Bye Bye !", score())
        return statement(txt).simple_card('game', txt)

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
