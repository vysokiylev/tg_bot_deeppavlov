# -*- coding: utf-8 -*- 
import telebot as telebot
from telebot import apihelper
from deeppavlov import configs, train_model
from deeppavlov.core.common.file import read_json
from deeppavlov.core.commands.infer import build_model
from deeppavlov.core.commands.train import train_evaluate_model_from_config


far = train_evaluate_model_from_config(configs.faq.tfidf_logreg_en_faq)
faq = build_model(configs.faq.tfidf_logreg_en_faq, download = True)
model_config = read_json("./config.json")
model_config["dataset_reader"]["data_path"] = "./faq_school_en.csv"
model_config["dataset_reader"]["data_url"] = None
faq = train_model(model_config)

bot = telebot.TeleBot('301914397:AAEmR8WlfzyxQT53zdpqHrSwR8iwaKEr-h8')

def GetAnswer(question):
    return faq([question])[0][0][0]

@bot.message_handler(content_types=['text'])
def get_text_messages(message):    
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        answer = GetAnswer(message.text)
        bot.send_message(message.from_user.id, answer)

bot.polling(none_stop=True, interval=0)