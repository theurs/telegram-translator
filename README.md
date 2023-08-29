# telegram-translator
Telegram bot for chatting in any language

Use this Telegram bot to translate conversations with people who speak different languages. To start a conversation, say "/start" to the bot and it will give you your number. To connect to someone else, type "/connect [number]". Everything you type will be sent to the other person translated into their language, and vice versa.


Example at https://t.me/chats_translator_bot


# install
Python 3.8+

sudo apt-get update
sudo apt install translate-shell python3-venv 


git clone https://github.com/theurs/telegram-translator.git

python -m venv .tb-tr
source ~/.tb-tr/bin/activate

pip install -r requirements.txt

config file

cfg.py
```
# Bot description, up to 512 symbols.
bot_description = """Telegram bot for chatting in any language

Use this Telegram bot to translate conversations with people who speak different languages. To start a conversation, say "/start" to the bot and it will give you your number. To connect to someone else, type "/connect [number]". Everything you type will be sent to the other person translated into their language, and vice versa."""


# a short description of the bot that is displayed on the bot's profile page and submitted
# along with a link when users share the bot. Up to 120 characters.
bot_short_description = """Use this Telegram bot to translate conversations with people who speak different languages."""


# Bot name (pseudonym), this is not a unique name, you can call it whatever you like,
# is not the name of the bot it responds to. Up to 64 characters.
bot_name = "Chat translator"


# list of admins who can use admin commands (/restart etc)
admins = [xxx,]


# telegram bot token
# @chats_translator_bot
token   = "xxx"
``````

start ./tb.py
