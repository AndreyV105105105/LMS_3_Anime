import telebot
from telebot import types

token = '6819222399:AAE9W2bLqFLTc-bhbSqOep7Pa-_68ocophA'
bot = telebot.TeleBot(token)
z = [['Берсерк', 'foto.jpg'], ['Реинкарнация Безработного', 'test_anime.jpg'], ['Ре Зеро', 'foto_3.jpg']]
k = 0
q = 0
s = {}

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
        addc = types.InlineKeyboardButton(text=f"({q + 1}/{len(z)})", callback_data='cifr')
        keyboard.add(add1, addc)
        bot.send_photo(chat_id, photo, caption=nazv, reply_markup=keyboard)
    elif m.text == v[1]:
        bot.send_message(m.chat.id, '💭 Здарова! \n\nНа данный момент, раздел «🌚 Дополнительно» находится в '
                                    'разработке. \n\n🏗🚧👷‍♂')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        global q
        print(q)
        global z
        if call.data == ">>":
            q += 1
            if q != len(z) - 1 and q != 0:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({q + 1}/{len(z)})", callback_data='cifr')
                keyboard.add(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({q + 1}/{len(z)})", callback_data='cifr')
                keyboard.add(add2, addc)

            nazv = z[q][0]
            photo = open(z[q][1], 'rb')
            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        elif call.data == "<<":
            q -= 1
            if q != 0 and q != len(z) - 1:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({q + 1}/{len(z)})", callback_data='cifr')
                keyboard.add(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                addc = types.InlineKeyboardButton(text=f"({q + 1}/{len(z)})", callback_data='cifr')
                keyboard.add(addc, add1)

            nazv = z[q][0]
            photo = open(z[q][1], 'rb')
            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
