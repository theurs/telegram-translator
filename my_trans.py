#!/usr/bin/env python3


import subprocess

from py_trans import PyTranslator

import utils


def translate_text(text, lang):
    """
    Translates the given text using the specified language.

    Args:
        text (str): The text to be translated.
        lang (str, optional): The language to translate the text to.

    Returns:
        str or None: The translated text if the translation was successful, otherwise same text.
    """
    x = PyTranslator()
    r = x.translate(text, lang)
    if r['status'] == 'success':
        return r['translation']
    return text
    

def translate_text2(text, lang):
    """
    Translates the given text using the specified language. Using trans utility.

    Args:
        text (str): The text to be translated.
        lang (str, optional): The language to translate the text to.

    Returns:
        str or None: The translated text if the translation was successful, otherwise same text.
    """
    process = subprocess.Popen(['trans', f':{lang}', '-b', text], stdout = subprocess.PIPE)
    output, error = process.communicate()
    r = output.decode('utf-8').strip()
    if error != None:
        return text
    return r


def translate(text, lang):
    """
    Translates the given text to the specified language.

    Args:
        text (str): The text to be translated.
        lang (str): The language to translate the text into.

    Returns:
        str: The translated text.
    """
    if 'windows' in utils.platform().lower():
        return translate_text(text, lang)
    else:
        return translate_text2(text, lang)


if __name__ == "__main__":
    text = "Вітаю! Я - інфармацыйная сістэма, якая можа адказаць на запытанні ў вас."
    
    print(translate(text, 'en'))
