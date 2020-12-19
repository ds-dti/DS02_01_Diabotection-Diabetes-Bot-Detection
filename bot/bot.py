#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from urllib import request

PORT = int(os.environ.get('PORT', 5000))
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token='------------'


updater = Updater(token,use_context=True)
dp = updater.dispatcher

qry = range(1)

def predict(update, context):
    update.message.reply_text("""Masukkan Informasi terkait berapa kali anda pernah gamil, berat badan (Kg), tinggi badan (Cm), usia (Tahun) dengan format berikut

Berapa kali hamil/Berat Badan (Kg)/ Tinggi (Cm)/ Usia (Tahun)

Contoh :
Jika anda pernah hamil sebanyak 2 kali, memiliki berat badan 60kg, dan tinggi 150cm, dan berusia  40 tahun

Maka silahkan ketik dengan format berikut

2/60/150/40

    """)
    return qry

def result(update, context):
    query = update.message.text.strip()
    a = query
    try:
        inp = a.split('/')
        preg = inp[0]
        weight = inp[1]
        height = inp[2]
        age = inp[3]
        url = f'http://feelfree10.pythonanywhere.com/personal_api?pregnancies={preg}&weight={weight}&height={height}&age={age}'
        response = request.urlopen(url)
        data = json.loads(response.read())
        c = data['result']
    except:
        c = 2

    if c == str(0):
        c = """Anda tidak memiliki kecenderungan memiliki diabetes. Tetap jaga kesehatan anda dengan baik.

Untuk informasi yang lebih lengkap silahkan kunjungi bit.ly/diabotection :)
        """
    elif c == str(1):
        c = """Anda memiliki kecenderungan memiliki diabetes. Harap lakukan pemeriksaan medis ke Laboratorium Medis Terdekat.

Untuk informasi yang lebih lengkap silahkan kunjungi bit.ly/diabotection :)
        """
    else :
        c = """Masukan data sesuai dengan format yang ditentukan"""

    text = f'{str(c)}'
    update.message.reply_text(text)
    return ConversationHandler.END

obrolan = ConversationHandler(
    entry_points = [CommandHandler('predict', predict)],
    states = {
        qry: [MessageHandler(Filters.text, result)]
    },
    fallbacks = []
)

def main():
    """Start the bot."""
    dp.add_handler(obrolan)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=token)
    updater.bot.setWebhook('https://yourappname.herokuapp.com/' + token)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
