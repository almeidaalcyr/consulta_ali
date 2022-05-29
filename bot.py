#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 28 22:20:12 2022

@author: alcyr
"""

from s import API_TOKEN
from ali import Consulta_aliexpress
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text("Alerta de preco - Ali express. Em desenvolvimento")

def help(update, context):
    update.message.reply_text("Alerta de preco - Ali express. Em desenvolvimento")

def alerta(update, context):
    item = update.message.text
    item = item.split(' ')

    i = Consulta_aliexpress(item[1])
    update.message.reply_text(i.getTitulo())

    if len(item) == 2:
        update.message.reply_text("*Opções:*")

        opcoes = i.listaOpcoes()
        for o in opcoes:
            opcao = str(o[0]) + ": " + o[5] + " " + o[6] + " (R$" + str(o[1]) + ")"
            update.message.reply_text(opcao)
    else:
        o = i.consultaPreco(i.getAtributos(int(item[2]))[0], i.getAtributos(int(item[2]))[1])
        opcao = str(o[0]) + ": " + o[5] + " " + o[6] + " (R$" + str(o[1]) + ")"
        update.message.reply_text(opcao)

def chatid(update, context):
    chat_id = update.message.chat.id
    update.message.reply_text(chat_id)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('alerta', alerta))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
