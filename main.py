import telebot
import sqlite3
from telebot import types

token = '6819222399:AAE9W2bLqFLTc-bhbSqOep7Pa-_68ocophA'
bot = telebot.TeleBot(token)
# vmesto_BD = [['Берсерк', 'data/all_anime/Berserk.png', 'https://animego.org/anime/berserk-313', ],
#              ['Реинкарнация Безработного', 'data/all_anime/Reincarnation of unemployed.jpg',
#               'https://animego.org/anime/reinkarnaciya-bezrabotnogo-istoriya-o-priklyucheniyah-v-drugom-mire-1690'],
#              ['Ре Зеро', 'data/all_anime/Re Zero.jpg',
#               'https://animego.org/anime/re-zhizn-v-alternativnom-mire-s-nulya-109']]

cout_of_anime = 4
# формат БД:
# nazv   0
# genre   1
# status  2
# year    3
# mangaka 4
# retell  5
# photo   6
# href    7


@bot.message_handler(commands=["start"])
def start(m):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('👺 Аниме')
    button2 = types.KeyboardButton('🌚 Дополнительно')
    keyboard.row(button1, button2)
    bot.send_message(m.chat.id, 'Описание бота, очень интересное', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def handle_text(m):
    v = ['👺 Аниме', '🌚 Дополнительно']
    chat_id = m.chat.id

    if m.text == v[0]:
        # global vmesto_BD
        index_v_BD = 0

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        addizbr = types.InlineKeyboardButton(text="⭐ Избранное", callback_data=f'izbran_anime|{index_v_BD}')
        addall = types.InlineKeyboardButton(text="🙄 Всё аниме", callback_data=f'all_anime|{index_v_BD}')
        keyboard.row(addizbr, addall)

        photo_start_anime = open('data/phones/start_anime.jpg', 'rb')

        bot.send_photo(chat_id, photo_start_anime, caption=f'🤠 Выбери раздел, который тебе нужен',
                       reply_markup=keyboard)

    elif m.text == v[1]:
        bot.send_message(m.chat.id, '💭 Здарова! \n\nНа данный момент, раздел «🌚 Дополнительно» находится в '
                                    'разработке. \n\n🏗🚧👷‍♂')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    info = call.data.split('|')
    callback = info[0]
    chat_id = call.from_user.id
    message_id = call.message.id
    # global vmesto_BD
    print(info)

    if call.message:
        if callback == ">>":
            index_v_BD = int(info[1])
            index_v_BD += 1

            con = sqlite3.connect("tg.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime
                        WHERE id = ?""", (index_v_BD + 1,)).fetchall()
            print(result)
            result = result[0]
            con.close()

            if index_v_BD != cout_of_anime - 1 and index_v_BD != 0:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{index_v_BD}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{index_v_BD}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{cout_of_anime})",
                                                  callback_data=f'cifr|{index_v_BD}')
                keyboard.row(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup()
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{index_v_BD}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{cout_of_anime})",
                                                  callback_data=f'cifr|{index_v_BD}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{index_v_BD}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'
            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        elif callback == "<<":
            index_v_BD = int(info[1])
            index_v_BD -= 1

            con = sqlite3.connect("tg.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime
                                    WHERE id = ?""", (index_v_BD + 1,)).fetchall()
            result = result[0]
            con.close()

            if index_v_BD != 0 and index_v_BD != cout_of_anime - 1:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{index_v_BD}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{index_v_BD}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{cout_of_anime})",
                                                  callback_data=f'cifr|{index_v_BD}')
                keyboard.row(add2, addc, add1)
            else:
                keyboard = types.InlineKeyboardMarkup()
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{index_v_BD}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{cout_of_anime})",
                                                  callback_data=f'cifr|{index_v_BD}')
                keyboard.row(addc, add1)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{index_v_BD}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'
            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)
        elif callback == "all_anime":

            index_v_BD = int(info[1])

            con = sqlite3.connect("tg.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime
                                    WHERE id = ?""", (index_v_BD + 1,)).fetchall()
            result = result[0]
            con.close()

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{index_v_BD}')
            addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{cout_of_anime})",
                                              callback_data=f'cifr|{index_v_BD}')
            keyboard.row(add1, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{index_v_BD}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'
            photo = open(result[6], 'rb')

            bot.delete_message(chat_id, message_id)

            bot.send_photo(chat_id, photo, caption=f'{nazv}', reply_markup=keyboard)
        elif callback == "cifr":
            pass
        elif callback == 'izbran_anime':
            bot.answer_callback_query(callback_query_id=call.id, text='На данный момент, раздел «⭐ Избранное» '
                                                                      'находится в '
                                                                      'разработке.\n\n🏗🚧👷‍♂')
        elif callback == 'back_to_menu':
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            addizbr = types.InlineKeyboardButton(text="⭐ Избранное", callback_data=f'izbran_anime|{0}')
            addall = types.InlineKeyboardButton(text="🙄 Всё аниме", callback_data=f'all_anime|{0}')
            keyboard.row(addizbr, addall)

            bot.delete_message(chat_id, message_id)

            photo_start_anime = open('data/phones/start_anime.jpg', 'rb')
            bot.send_photo(chat_id, photo_start_anime, caption=f'🤠 Выбери раздел, который тебе нужен',
                           reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
