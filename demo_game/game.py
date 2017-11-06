from flask import Flask
from flask_ask import Ask, statement, session, question
import logging
import os
import random

import boto3
from boto3.dynamodb.conditions import Key, Attr


app = Flask(__name__)
ask = Ask(app, '/')


logging.getLogger('flask_ask').setLevel(logging.DEBUG)
choices = ["rock", "scissors", "paper"]
DYNAMODB_HISTORY_TABLE = 'game_history'

win_states = {
    'rock':'scissors',
    'scissors': 'paper',
    'paper': 'rock',
}

class GameHistory(object):


    def __init__(self, user_id):
        self.user_id = user_id
        self._conn = boto3.resource("dynamodb")
        self._table = self._conn.Table(DYNAMODB_HISTORY_TABLE)
        self._history = []
        self._refresh_history()

    def _refresh_history(self):
        response = self._table.query(
            KeyConditionExpression=Key('user_id').eq(self.user_id)
        )
        self._history = response['Items']

    @property
    def game_number(self):
        return len(self._history)

    def add_game_state(self, game_state, game_score):
        self._table.put_item(
            Item={
                'user_id': self.user_id,
                'game_number': self.game_number + 1,
                'game_state': game_state,
                'game_score': game_score
            }
        )
        self._refresh_history()

    def load_score(self):
        return "You {}, Alexa {}".format(sum([1 for h in self._history if h['game_score'] == 1]),
                                         sum([1 for h in self._history if h['game_score'] == -1]))





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
    history = GameHistory(session['user']['userId'])
    history.add_game_state(list(score), score[2])


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
        txt = "Sorry but I do not understand, please repeat" + e.message
    return question(txt).simple_card('game', txt)


@ask.launch
def launch():
    txt = "Welcome to rock paper scissors demo game. Do you want to play?"
    return question(txt).simple_card('start game', txt)

@ask.intent('PlayerScore')
def player_score(player_choice):
        history = GameHistory(session['user']['userId'])
        history.load_score()
        return question(history.load_score())

@ask.intent('EndGame')
def end():
        history = GameHistory(session['user']['userId'])
        txt = "{} {}".format(" Bye Bye !", history.load_score())
        return statement(txt).simple_card('game', txt)

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=8080)
