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

log.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=log.INFO)
logger = log.getLogger(__name__)

def command_start(update: Update, context: CallbackContext):
	bot = context.bot
	cid = update.message.chat_id
	bot.send_message(cid, "Bot para collectores")

def main():	
	BOT_TOKEN = os.environ.get('token', None)
	if BOT_TOKEN is None :
		config = configparser.ConfigParser()
		config.read('init.ini')
		BOT_TOKEN = config['ENVIROMENT']['TOKEN']
	print(BOT_TOKEN)
	updater = Updater(BOT_TOKEN, use_context=True)

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", command_start))
	updater.start_polling(timeout=30)
	
	updater.idle()

if __name__ == '__main__':
    main()
