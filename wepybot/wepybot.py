#######################################################
# By Matteo Fava                                      #
# Created: 01/20/2022                                 #
# Finished: 01/25/2022                                #
# This code will be the main code of the telegram bot #
#######################################################

#imports
from logging import basicConfig, getLogger, INFO
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from json import load, dump
from os.path import dirname

#import functions from functions.py
from api_functions import Current, outputForecast, outputForecastDay

#telegram token
tg_token="" #Insert here telegram token
dir = dirname(__file__)

#store user data
with open(f"{dir}/users.json", "r") as file:
    user = load(file)
locations=user["locations"]
users=user["users"]

# Enable logging
basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=INFO
)
logger = getLogger(__name__)

#define updater
updater = Updater(tg_token, use_context=True)

#update users.json
def dumpInUsers():
     with open(f"{dir}/users.json", "w") as file:
        dump(user, file)

#start function
def start(update: Update, context: CallbackContext):
    chat_id = chat_id = update.effective_user.id
    users.append(chat_id)
    dumpInUsers()
    n = set(users)
    users_n = len(n)
    print("Number of users:", users_n)
    update.message.reply_text(
        "Hello welcome to the bot! For a brief description on how to use the bot: /help.")

#help function
def help(update: Update, context: CallbackContext):
    help="""To interact with the bot use this commands:
** "location" can be the name of the place or also coordinates like "45.4642,9.1900" **
/start - starts the bot.
/help - to know how to use the bot.
/about - how and why this bot was created.
/setlocation + "location" - to set the favorite location.
/current + "location" (or just /current if a fav. location has been saved) to know the current weather.
/today + "location" (or just /today if a fav. location has been saved) to know today's weather.
/forecast + "location" (or just /forecast if a fav. location has been saved) to get a 2 day's forecast.
    """
    update.message.reply_text(help)

#about function
def about(update: Update, context: CallbackContext):
    update.message.reply_text("This bot was created as a final project for a Computer Science Class! It was built using Python, with data from weatherapi.com and hosted on heroku.com. To feedback updates or bug fixes email to: weatherbot.developer@gmail.com")

#answer with current weather in one location
def current(update: Update,  context: CallbackContext):
    chat_id = update.effective_user.id
    if not context.args:
        if not chat_id in locations:
            update.message.reply_text('Oops, no location given! /help for more info or /setlocation + "location" to save a favorite location.')
        else:
            city = locations[chat_id]
            update.message.reply_text(Current(city))
    else:
        city = update.message.text.partition(' ')[2]
        update.message.reply_text(Current(city))

#answer with the weather today in the location
def today(update: Update,  context: CallbackContext):
    chat_id = update.effective_user.id
    if not context.args:
        if not chat_id in locations:
            update.message.reply_text('Oops, no location given! /help for more info or /setlocation + "location" to save a favorite location.')
        else:
            city = locations[chat_id]
            update.message.reply_text(outputForecastDay(city, 1))
    else:
        city = update.message.text.partition(' ')[2]
        update.message.reply_text(outputForecastDay(city, 1))

#answer with the weather forecast in the location
def forecast(update: Update,  context: CallbackContext):
    chat_id = update.effective_user.id
    if not context.args:
        if not chat_id in locations:
            update.message.reply_text('Oops, no location given! /help for more info or /setlocation + "location" to save a favorite location.')
        else:
            city = locations[chat_id]
            update.message.reply_text(outputForecast(city, 3))
    else:
        city = update.message.text.partition(' ')[2]
        update.message.reply_text(outputForecast(city, 2))

#set a favorite location for each user
def setlocation(update: Update,  context: CallbackContext):
    chat_id = update.effective_user.id
    if not context.args:
       update.message.reply_text('No location given! /help for more info')
    else:
        city= update.message.text.partition(' ')[2]
        locations[chat_id]=(city)
        dumpInUsers()
        update.message.reply_text('Favorite location updated to:  '+locations[chat_id])

#unknown
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry, unknown command! Try /help.")

#unknown text
def unknown_text(update: Update):
    update.message.reply_text(update.message.text)


#add handlers for the messages
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('current', current))
updater.dispatcher.add_handler(CommandHandler('today', today))
updater.dispatcher.add_handler(CommandHandler('forecast', forecast))
updater.dispatcher.add_handler(CommandHandler('setlocation', setlocation))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

#filter out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

#start the bot
if __name__ == "__main__":
    updater.start_polling()
    updater.idle()
