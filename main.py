import telebot
from telebot import types

token = '6819222399:AAE9W2bLqFLTc-bhbSqOep7Pa-_68ocophA'
bot = telebot.TeleBot(token)
vmesto_BD = [['Берсерк', 'data/all_anime/Berserk.png', 'https://animego.org/anime/berserk-313', ], ['Реинкарнация Безработного', 'data/all_anime/Reincarnation of unemployed.jpg', 'https://animego.org/anime/reinkarnaciya-bezrabotnogo-istoriya-o-priklyucheniyah-v-drugom-mire-1690'], ['Ре Зеро', 'data/all_anime/Re Zero.jpg', 'https://animego.org/anime/re-zhizn-v-alternativnom-mire-s-nulya-109']]

# формат БД: ['название', 'имя картинки', 'ссылка']
# формат может в будущем дополняться
index_v_BD = 0

@bot.message_handler(commands=["start"])
def start(m, res=False):
    keyboard = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('👺 Аниме')
    button2 = types.KeyboardButton('🌚 Дополнительно')
    keyboard.add(button1, button2)
    bot.send_message(m.chat.id, 'Описание бота, очень интересное', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    v = ['👺 Аниме', '🌚 Дополнительно']
    chat_id = m.chat.id

    if m.text == v[0]:
        photo_start_anime = open('data/phones/start_anime.jpg', 'rb')
        addizbr = types.InlineKeyboardButton(text="⭐ Избранное", callback_data=f'izbran_anime')
        addall = types.InlineKeyboardButton(text="⭐ Избранное", callback_data='all_anime')
        global vmesto_BD
        global index_v_BD
        nazv = vmesto_BD[index_v_BD][0]
        photo = open(vmesto_BD[index_v_BD][1], 'rb')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
        addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{len(vmesto_BD)})", callback_data='cifr')
        keyboard.row(add1, addc)
        href = vmesto_BD[index_v_BD][2]
        addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
        keyboard.row(addhref)
        bot.send_photo(chat_id, photo, caption=nazv, reply_markup=keyboard)
    elif m.text == v[1]:
        bot.send_message(m.chat.id, '💭 Здарова! \n\nНа данный момент, раздел «🌚 Дополнительно» находится в '
                                    'разработке. \n\n🏗🚧👷‍♂')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        global index_v_BD
        global vmesto_BD
        if call.data == ">>":
            index_v_BD += 1
            if index_v_BD != len(vmesto_BD) - 1 and index_v_BD != 0:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{len(vmesto_BD)})", callback_data='cifr')
                keyboard.row(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup()
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{len(vmesto_BD)})", callback_data='cifr')
                keyboard.row(add2, addc)
            href = vmesto_BD[index_v_BD][2]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)
            nazv = vmesto_BD[index_v_BD][0]
            photo = open(vmesto_BD[index_v_BD][1], 'rb')
            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        elif call.data == "<<":
            index_v_BD -= 1
            if index_v_BD != 0 and index_v_BD != len(vmesto_BD) - 1:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                add2 = types.InlineKeyboardButton(text="<<", callback_data='<<')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{len(vmesto_BD)})", callback_data='cifr')
                keyboard.row(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data='>>')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{len(vmesto_BD)})", callback_data='cifr')
                keyboard.row(addc, add1)
            href = vmesto_BD[index_v_BD][2]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)
            nazv = vmesto_BD[index_v_BD][0]
            photo = open(vmesto_BD[index_v_BD][1], 'rb')
            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=call.message.chat.id, message_id=call.message.message_id,
                                   reply_markup=keyboard)
        elif call.data == "all_anime":
            pass

bot.polling(none_stop=True, interval=0)
