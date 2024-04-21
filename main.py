import telebot
import sqlite3
from telebot import types
from data.visov.tg_genre import genre
from data.visov.tg_mangaka import name
from data.visov.tg_status import status
from data.visov.tg_title import title
from data.visov.tg_year import year

from data.visov.all_genres import all_genre
from data.visov.all_statuses import all_statuses
from data.visov.basa import basa

from data.visov.tg_delete_saved import remove_anime_number_by_id
from data.visov.tg_read_saved import read_saved
from data.visov.tg_write_saved import add_anime_number

token = '6819222399:AAE9W2bLqFLTc-bhbSqOep7Pa-_68ocophA'
bot = telebot.TeleBot(token)

slovar_index_v_BD = {}
connn = sqlite3.connect('data/BD/tg.sqlite')
currr = connn.cursor()
reqqq = currr.execute(f"""SELECT title, genre, status, year, mangaka, retell, image, link FROM anime""").fetchall()
connn.close()

count_of_anime = len(reqqq)
# формат БД:
# nazv    0
# genre   1
# status  2
# year    3
# mangaka 4
# retell  5
# photo   6
# href    7
# id      8


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
        if chat_id not in slovar_index_v_BD:
            slovar_index_v_BD[chat_id] = 0
        else:
            slovar_index_v_BD[chat_id] = 0
        index_v_BD = slovar_index_v_BD[chat_id]
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
    pravo = callback.split('>>')
    levo = callback.split('<<')
    chat_id = call.from_user.id
    message_id = call.message.id
    print(info)

    statuses = all_statuses()

    if call.message:
        if callback == ">>":
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] += 1

            index_v_BD = slovar_index_v_BD[chat_id]
            result = basa(index_v_BD)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != count_of_anime - 1 and index_v_BD != 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            addfilter = types.InlineKeyboardButton("Фильтр", callback_data=f'filter|{result[8]}')
            keyboard.row(addfilter)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        elif callback == "<<":
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] -= 1
            index_v_BD = slovar_index_v_BD[chat_id]

            result = basa(index_v_BD)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_anime - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(addc, add1)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            addfilter = types.InlineKeyboardButton("Фильтр", callback_data=f'filter|{result[8]}')
            keyboard.row(addfilter)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)
        elif callback == "all_anime":
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            index_v_BD = slovar_index_v_BD[chat_id]

            result = basa(index_v_BD)
            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_anime - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            elif index_v_BD == 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add1, addc)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            addfilter = types.InlineKeyboardButton("Фильтр", callback_data=f'filter|{result[8]}')
            keyboard.row(addfilter)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.delete_message(chat_id, message_id)

            bot.send_photo(chat_id, photo, caption=f'{nazv}', reply_markup=keyboard)
        elif callback == "cifr":
            pass

        elif callback == 'izbran_anime':
            if len(read_saved(str(chat_id))) == 0:
                bot.answer_callback_query(callback_query_id=call.id, text='У Вас в разделе «⭐ Избранное» '
                                                                          'ничего нет.\n\n🏗🚧👷‍♂')
            else:
                izb = read_saved(str(chat_id))
                if len(izb) != 0:
                    izb = izb[0]
                if chat_id not in slovar_index_v_BD:
                    slovar_index_v_BD[chat_id] = 0
                else:
                    slovar_index_v_BD[chat_id] = 0
                index_v_BD = slovar_index_v_BD[chat_id]

                result = izb[index_v_BD]

                count_of_iz = len(izb)

                keyboard = types.InlineKeyboardMarkup()

                addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
                for uuu in izb:
                    if result[8] == uuu[-1]:
                        addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                           callback_data=f'iz_del|{result[8]}')
                        break
                keyboard.row(addiz)

                if len(izb) != 1:
                    if index_v_BD != 0 and index_v_BD != count_of_iz - 1:
                        add1 = types.InlineKeyboardButton(text=">>", callback_data=f'izbran>>|{result[8]}')
                        add2 = types.InlineKeyboardButton(text="<<", callback_data=f'izbran<<|{result[8]}')
                        addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_iz})",
                                                          callback_data=f'cifr|{result[8]}')
                        keyboard.row(add2, addc, add1)
                    elif index_v_BD == 0:
                        add1 = types.InlineKeyboardButton(text=">>", callback_data=f'izbran>>|{result[8]}')
                        addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_iz})",
                                                          callback_data=f'cifr|{result[8]}')
                        keyboard.row(add1, addc)
                    else:
                        add2 = types.InlineKeyboardButton(text="<<", callback_data=f'izbran<<|{result[8]}')
                        addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_iz})",
                                                          callback_data=f'cifr|{result[8]}')
                        keyboard.row(add2, addc)
                else:
                    addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_iz})",
                                                      callback_data=f'cifr|{result[8]}')
                    keyboard.row(addc)

                href = result[7]
                addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
                keyboard.row(addhref)

                addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
                keyboard.row(addback)

                nazv = f'{result[0]}\n\n{result[5]}'

                photo = open(result[6], 'rb')

                bot.delete_message(chat_id, message_id)

                bot.send_photo(chat_id, photo, caption=f'{nazv}', reply_markup=keyboard)


        elif pravo[0] == 'izbran':
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] += 1
            index_v_BD = slovar_index_v_BD[chat_id]
            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            print(izb)
            result = izb[index_v_BD]

            count_of_statuses = len(izb)

            keyboard = types.InlineKeyboardMarkup()


            print(result)
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != count_of_statuses - 1 and index_v_BD != 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'izbran>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'izbran<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'izbran<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)
        elif levo[0] == 'izbran':
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] -= 1
            index_v_BD = slovar_index_v_BD[chat_id]

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            result = izb[index_v_BD]

            count_of_statuses = len(izb)

            keyboard = types.InlineKeyboardMarkup()

            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_statuses - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'izbran>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'izbran<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'izbran>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(addc, add1)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)


        elif callback == 'back_to_menu':
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            addizbr = types.InlineKeyboardButton(text="⭐ Избранное", callback_data=f'izbran_anime|{0}')
            addall = types.InlineKeyboardButton(text="🙄 Всё аниме", callback_data=f'all_anime|{0}')
            keyboard.row(addizbr, addall)

            bot.delete_message(chat_id, message_id)

            photo_start_anime = open('data/phones/start_anime.jpg', 'rb')

            bot.send_photo(chat_id, photo_start_anime, caption=f'🤠 Выбери раздел, который тебе нужен',
                           reply_markup=keyboard)
        elif callback == 'filter':
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            index_v_BD = slovar_index_v_BD[chat_id]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            # add1 = types.InlineKeyboardButton(text="Жанр", callback_data=f'genre|{index_v_BD}')
            # add2 = types.InlineKeyboardButton(text="Мангака", callback_data=f'name|{0}')
            add3 = types.InlineKeyboardButton(text="Статус", callback_data=f'status|{0}')
            # add4 = types.InlineKeyboardButton(text="Год", callback_data=f'year|{0}')
            # add5 = types.InlineKeyboardButton(text="Название", callback_data=f'title|{index_v_BD}')
            addback = types.InlineKeyboardButton(text="Назад", callback_data=f'all_anime|{0}')

            # keyboard.row(add1)
            # keyboard.row(add2)
            keyboard.row(add3)
            # keyboard.row(add4)
            # keyboard.row(add5)
            keyboard.row(addback)

            bot.delete_message(chat_id, message_id)

            photo = open('data/phones/filter.jpg', 'rb')

            bot.send_photo(chat_id, photo, caption=f'Что ты ищешь?',
                           reply_markup=keyboard)
        elif callback == 'status':
            keys_status = list(statuses.keys())
            print(keys_status)
            keyboard = types.InlineKeyboardMarkup()
            z = []
            for i in range(len(keys_status)):
                z.append(types.InlineKeyboardButton(text=f"{keys_status[i]}", callback_data=f'{keys_status[i]}|{0}'))
                if i == len(keys_status) - 1 or len(z) == 4:
                    if len(z) == 4:
                        keyboard.row(z[0], z[1], z[2], z[3])
                    elif len(z) == 3:
                        keyboard.row(z[0], z[1], z[2])
                    elif len(z) == 2:
                        keyboard.row(z[0], z[1])
                    else:
                        keyboard.row(z[0])
                    z = []

            bot.delete_message(chat_id, message_id)

            bot.send_message(chat_id, f'Выбери', reply_markup=keyboard)

        elif callback in all_statuses():
            result_all = status(callback)

            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] = 0
            index_v_BD = slovar_index_v_BD[chat_id]

            result = result_all[index_v_BD]

            count_of_statuses = len(result_all)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if len(result_all) != 1:
                if index_v_BD != 0 and index_v_BD != count_of_statuses - 1:
                    add1 = types.InlineKeyboardButton(text=">>", callback_data=f'status>>{callback}>>|{result[8]}')
                    add2 = types.InlineKeyboardButton(text="<<", callback_data=f'status<<{callback}<<|{result[8]}')
                    addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                      callback_data=f'cifr|{result[8]}')
                    keyboard.row(add2, addc, add1)
                elif index_v_BD == 0:
                    add1 = types.InlineKeyboardButton(text=">>", callback_data=f'status>>{callback}>>|{result[8]}')
                    addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                      callback_data=f'cifr|{result[8]}')
                    keyboard.row(add1, addc)
                else:
                    add2 = types.InlineKeyboardButton(text="<<", callback_data=f'status<<{callback}<<|{result[8]}')
                    addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                      callback_data=f'cifr|{result[8]}')
                    keyboard.row(add2, addc)
            else:
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.delete_message(chat_id, message_id)

            bot.send_photo(chat_id, photo, caption=f'{nazv}', reply_markup=keyboard)
        elif pravo[0] == 'status':
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] += 1
            index_v_BD = slovar_index_v_BD[chat_id]
            result_all = status(pravo[1])

            result = result_all[index_v_BD]

            count_of_statuses = len(result_all)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != count_of_statuses - 1 and index_v_BD != 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'status>>{pravo[1]}>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'status<<{pravo[1]}<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'status<<{pravo[1]}<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)
        elif levo[0] == 'status':
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] -= 1
            index_v_BD = slovar_index_v_BD[chat_id]

            result_all = status(levo[1])

            result = result_all[index_v_BD]

            count_of_statuses = len(result_all)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_statuses - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'status>>{levo[1]}>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'status<<{levo[1]}<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            else:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'status>>{levo[1]}>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_statuses})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(addc, add1)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)

        elif callback == 'iz_ad':
            id = info[1]
            print(id)
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] = int(info[1]) - 1
            index_v_BD = slovar_index_v_BD[chat_id]

            result = basa(int(info[1]) - 1)

            add_anime_number(str(chat_id), id)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного", callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_anime - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            elif index_v_BD == 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add1, addc)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            addfilter = types.InlineKeyboardButton("Фильтр", callback_data=f'filter|{result[8]}')
            keyboard.row(addfilter)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)
        elif callback == 'iz_del':
            id = info[1]
            print(id)
            if chat_id not in slovar_index_v_BD:
                slovar_index_v_BD[chat_id] = 0
            else:
                slovar_index_v_BD[chat_id] = int(info[1]) - 1
            index_v_BD = slovar_index_v_BD[chat_id]

            result = basa(int(info[1]) - 1)

            remove_anime_number_by_id(str(chat_id), id)

            keyboard = types.InlineKeyboardMarkup()

            izb = read_saved(str(chat_id))
            if len(izb) != 0:
                izb = izb[0]
            addiz = types.InlineKeyboardButton(text="Добавить в избранное", callback_data=f'iz_ad|{result[8]}')
            for uuu in izb:
                if result[8] == uuu[-1]:
                    addiz = types.InlineKeyboardButton(text="Удалить из избранного",
                                                       callback_data=f'iz_del|{result[8]}')
                    break
            keyboard.row(addiz)

            if index_v_BD != 0 and index_v_BD != count_of_anime - 1:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc, add1)
            elif index_v_BD == 0:
                add1 = types.InlineKeyboardButton(text=">>", callback_data=f'>>|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add1, addc)
            else:
                add2 = types.InlineKeyboardButton(text="<<", callback_data=f'<<|{result[8]}')
                addc = types.InlineKeyboardButton(text=f"({index_v_BD + 1}/{count_of_anime})",
                                                  callback_data=f'cifr|{result[8]}')
                keyboard.row(add2, addc)

            href = result[7]
            addhref = types.InlineKeyboardButton("👁 Смотреть", url=f'{href}')
            keyboard.row(addhref)

            addback = types.InlineKeyboardButton("🔙 Назад в меню", callback_data=f'back_to_menu|{result[8]}')
            keyboard.row(addback)

            addfilter = types.InlineKeyboardButton("Фильтр", callback_data=f'filter|{result[8]}')
            keyboard.row(addfilter)

            nazv = f'{result[0]}\n\n{result[5]}'

            photo = open(result[6], 'rb')

            bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=photo, caption=nazv),
                                   chat_id=chat_id, message_id=message_id,
                                   reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)
