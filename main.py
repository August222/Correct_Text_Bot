import telebot
from telebot import types
import autocorrect
from autocorrect import Speller
from settings import token

bot = telebot.TeleBot(token=token)


# START BUTTONS
@bot.message_handler(commands=["start"])
def start_buttons(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button_ru = types.InlineKeyboardButton("ru", callback_data="ru_id")
    button_en = types.InlineKeyboardButton("en", callback_data="en_id")
    markup.add(button_ru, button_en)
    hello = f"Привет, {message.from_user.first_name}!\nВыбери язык, на котором будешь печатать."
    bot.send_message(message.chat.id, hello, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback(callback):
    if callback.data == "ru_id":
        bot.send_message(callback.message.chat.id, "Отлично!\nОтправь мне текст/слово которое хочешь исправить.")
    elif callback.data == "en_id":
        bot.send_message(callback.message.chat.id, "Извини, пока не понимаю английский язык!\nПопробуй напечатать на русском.")


# CORRECTING TEXT
@bot.message_handler(content_types=["text"])
def correct_user_text(message):
    spell = Speller("ru")
    changed_text = spell(f"{message.text}")
    bot.send_message(message.chat.id, f"{changed_text}")


bot.polling(none_stop=True)