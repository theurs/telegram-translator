#!/usr/bin/env python3

import os
import threading

import telebot

import cfg
import my_dic
import my_log
import my_trans
import utils


# set the working folder = the folder where the script is located
os.chdir(os.path.abspath(os.path.dirname(__file__)))


bot = telebot.TeleBot(cfg.token, skip_pending=True)


# folder for permanent dictionaries, bot memory
if not os.path.exists('db'):
    os.mkdir('db')


# saved pairs of user:language
DB = my_dic.PersistentDict('db/db.pkl')
# saved pairs user:user
CONNECTS = my_dic.PersistentDict('db/connects.pkl')


@bot.message_handler(commands=['restart']) 
def restart(message: telebot.types.Message):
    """bot stop. after stopping it will have to restart the systemd script"""
    if message.from_user.id in cfg.admins:
        bot.stop_polling()
    else:
        bot.reply_to(message, 'For admins only.')


@bot.message_handler(commands=['start'])
def send_welcome_start(message: telebot.types.Message):
    # Отправляем приветственное сообщение

    my_log.log_echo(message)

    user_id = message.from_user.id
    
    default_lang = message.from_user.language_code or 'en'
    if user_id not in DB:
        DB[user_id] = default_lang

    help = f'Your telegram ID: <b>{user_id}</b>\n\nYour language: <b>{DB[user_id]}</b>, use /language command to change it'

    bot.reply_to(message, help, parse_mode='HTML')
    my_log.log_echo(message, help)


@bot.message_handler(commands=['language', 'lang'])
def language(message: telebot.types.Message):
    """Change language"""
    user_id = message.from_user.id
    if user_id not in DB:
        DB[user_id] = message.from_user.language_code or 'en'

    help = f'''/language language code

Current language: <b>{DB[user_id]}</b>

Example:

<code>/language es</code>
<code>/language en</code>
<code>/language ru</code>
<code>/language fr</code>

https://en.wikipedia.org/wiki/Template:Google_translation
'''


    try:
        new_lang = message.text.split(' ')[1].strip()
    except IndexError:
        bot.reply_to(message, help, parse_mode='HTML', disable_web_page_preview=True)
        return
    
    DB[user_id] = new_lang
    bot.reply_to(message, 'Language changed.')


@bot.message_handler(commands=['connect', 'con', 'c'])
def connect_to_user(message: telebot.types.Message) -> None:
    """Connect to user"""
    try:
        user = message.text.split(' ')[1]
        CONNECTS[message.from_user.id] = int(user)
        CONNECTS[int(user)] = message.from_user.id
        bot.reply_to(message, f'Connected to {user}.')
        return
    except IndexError:
        help = '/connect user ID to talk to'
        bot.reply_to(message, help, parse_mode='HTML')


@bot.message_handler(func=lambda message: True)
def echo_all(message: telebot.types.Message) -> None:
    """Text message handler"""
    thread = threading.Thread(target=do_task, args=(message,))
    thread.start()
def do_task(message):
    """Text message handler threaded"""
    user_id = message.from_user.id
    if user_id in CONNECTS:
        to_user_id = CONNECTS[user_id]
        if to_user_id in DB:
            lang = DB[to_user_id]
        else:
            bot.reply_to(message, 'I dont know who is it. This person have to say /start to me.')
            return
    else:
        bot.reply_to(message, 'Not connected, use /connect command first')
        return

    translated = my_trans.translate(message.text, lang)

    bot.send_message(to_user_id, translated, disable_notification=True)

    my_log.log_echo(message)
    my_log.log_echo(message, translated)


def set_default_commands():
    """
    Reads a file containing a list of commands and their descriptions,
    and sets the default commands for the bot.
    """
    commands = []
    with open('commands.txt', encoding='utf-8') as file:
        for line in file:
            try:
                command, description = line[1:].strip().split(' - ', 1)
                if command and description:
                    commands.append(telebot.types.BotCommand(command, description))
            except Exception as error:
                print(error)
    bot.set_my_commands(commands)

    bot_name = bot.get_my_name().name.strip()
    description = bot.get_my_description().description.strip()
    short_description = str(bot.get_my_short_description().short_description).strip()

    new_bot_name = cfg.bot_name.strip()
    new_description = cfg.bot_description.strip()
    new_short_description = cfg.bot_short_description.strip()

    if bot_name != new_bot_name:
        if not bot.set_my_name(cfg.bot_name):
            my_log.log2(f'Failed to set bot name: {cfg.bot_name}')
    if description != new_description:
        if not bot.set_my_description(cfg.bot_description):
            my_log.log2(f'Failed to set bot description: {cfg.bot_description}')
    if short_description != new_short_description:
        if not bot.set_my_short_description(cfg.bot_short_description):
            my_log.log2(f'Failed to set bot short description: {cfg.bot_short_description}')


def main():
    """
    Runs the main function, which sets default commands and starts polling the bot.
    """
    set_default_commands()
    bot.polling(timeout=90, long_polling_timeout=90)


if __name__ == '__main__':
    main()
