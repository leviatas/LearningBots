#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Peluffo"

import json
import logging as log
import random
import re
from random import randrange, choice
from time import sleep
from uuid import uuid4

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update, \
	InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (InlineQueryHandler, Updater, CommandHandler, \
	CallbackQueryHandler, MessageHandler, Filters, CallbackContext)
from telegram.utils.helpers import mention_html, escape_markdown

import traceback
import sys
import os
import configparser

from multiprocessing import Process

from telethon import TelegramClient, events, types, functions, Button
from telethon.sessions import StringSession

# Configuracion para logeo de datos en Heroku
log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO)
logger = log.getLogger(__name__)

# 1 - Cargo variables de entorno
API_ID = os.environ.get('api_id', None)
API_HASH = os.environ.get('api_hash', None)
STRING_SESSION = os.environ.get('STRING_SESSION', None)
BOT_TOKEN = os.environ.get('bot_token', None)

# 2 - Si no estan las obtengo del config, esto lo uso para probar local
if API_ID is None or API_HASH is None:
	config = configparser.ConfigParser()
	config.read('init.ini')
	API_ID = int(config['ENVIROMENT']['TG_API_ID'])
	API_HASH = config['ENVIROMENT']['TG_API_HASH']
	STRING_SESSION = config['ENVIROMENT']['STRING_SESSION']
	BOT_TOKEN = config['ENVIROMENT']['BOT_TOKEN']

#--------------------------------- BOT --------------------------------------

def command_start(update: Update, context: CallbackContext):
	bot = context.bot
	cid = update.message.chat_id
	bot.send_message(cid, "Bot para aprender")

def bot_main():
	updater = Updater(BOT_TOKEN, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", command_start))
	updater.start_polling(timeout=30)	
	updater.idle()

#-------------------------------FIN BOT ------------------------------------

#------------------------------ USER BOT -----------------------------------
client1 = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

# Esto hace que escuche en "Mensajes guardados" y solo mensajes mios (outgoing)
@events.register(events.NewMessage(chats='me', outgoing=True))
async def me_handler(event):
	# Logeo en Heroku que mensaje entro.
	logger.info(f"New message {event.raw_text}")
	# Que cuenta de telegram recibio el mensaje? La obtengo.
	client = event.client
	# El mensaje decia "Hola"?
	if event.raw_text == 'Hola':
		# Entonces respondo ¿Cómo estas?
		await client.send_message('me', '¿Cómo estas?')
	# El mensaje decia "Todo bien"?
	if event.raw_text == 'Todo bien':
		# Entonces respondo ¿Me alegro?
		await client.send_message('me', 'Me alegro')

# Agrego al cliente la capacidad de escuchar los mensajes de "Mensajes guardados"
client1.add_event_handler(me_handler)

#------------------------------ FIN USER BOT -------------------------------

# Configuro para que se puede usar el bot y el user bot al mismo tiempo.
def loop_a():
    while 1:
        sleep(0.01)
        client1.start()

def loop_b():
    while 1:
        bot_main()


if __name__ == '__main__':
    p1 = Process(target=loop_a).start()
    p2 = Process(target=loop_b).start()