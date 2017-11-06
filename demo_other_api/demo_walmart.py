from wapy.api import Wapy
key = "<WALMART API KEY>" # go to https://developer.walmartlabs.com/
wapy = Wapy(key)

from flask import Flask, render_template
from flask_ask import Ask, statement, session, question
import logging
import os

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.intent('SearchIntent')
def choice(firstsearchterm="", secondsearchterm="", thirdsearchterm=""):
    if firstsearchterm is None:
        firstsearchterm = ""
    if secondsearchterm is None:
        secondsearchterm = ""
    if thirdsearchterm is None:
        thirdsearchterm = ""
    res = " ".join([firstsearchterm, secondsearchterm, thirdsearchterm])
    print res
    res = wapy.search(res)
    txt = render_template('products_list', products=res)
    return question(txt).standard_card(title='Search result:',
                       text="{} price {}$".format( res[0].name,  res[0].sale_price) ,
                       small_image_url=res[0].thumbnail_image,
                       large_image_url=res[0].large_image)

@ask.launch
def launch():
    txt = "What are you loking for?"
    return question(txt)


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=8080)

