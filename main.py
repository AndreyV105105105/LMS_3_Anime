import telebot
from telebot import types

token = '6819222399:AAE9W2bLqFLTc-bhbSqOep7Pa-_68ocophA'
bot = telebot.TeleBot(token)
z = [['Берсерк', 'foto.jpg'], ['Реинкарнация Безработного', 'test_anime.jpg'], ['Ре Зеро', 'foto_3.jpg']]
k = 0
q = 0


@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.ReplyKeyboardMarkup(row_width=6)
    button1 = types.KeyboardButton('👺 Аниме')
    button2 = types.KeyboardButton('🌚 Дополнительно')
    keyboard.add(button1, button2)
    bot.send_message(m.chat.id, 'Описание бота, очень интересное', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    v = ['👺 Аниме', '🌚 Дополнительно']
    chat_id = m.chat.id
    if m.text == v[0]:
        global z
        global q
        nazv = z[q][0]
        photo = open(z[q][1], 'rb')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
        keyboard.add(add1)
        bot.send_photo(chat_id, photo, caption=nazv, reply_markup=keyboard)
        q += 1
        if q == len(z):
            q = 0
    elif m.text == v[1]:
        bot.send_message(m.chat.id, '💭 Здарова! \n\nНа данный момент, раздел «🌚 Дополнительно» находится в '
                                    'разработке. \n\n🏗🚧👷‍♂')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == ">>":
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            add = types.InlineKeyboardButton(text=">>", callback_data='>>')
            keyboard.add(add)
            global q
            global z
            nazv = z[q][0]
            photo = open(z[q][1], 'rb')
            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
            q += 1
            if q == len(z):
                q = 0
        elif call.data == "button2":
            bot.send_message(call.message.chat.id, "Вы нажали на вторую кнопку.")


bot.polling(none_stop=True, interval=0)
