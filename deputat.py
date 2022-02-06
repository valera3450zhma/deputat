import datetime
import random
import res
from telebot import types


class Deputat(object):
    def __init__(self, db_object, db_connection, bot):
        self.db_object = db_object
        self.db_connection = db_connection
        self.bot = bot

    # starts elections (а шо)
    def _start_elections_(self, call):
        # first, check if user is admin, because start the elections can ONLY an admin
        bot = self.bot
        db_object = self.db_object
        user_id = call.from_user.id
        chat_id = str(call.message.chat.id)
        is_admin = False
        admins_t = bot.get_chat_administrators(call.message.chat.id)  # get admins list
        for admin in admins_t:
            if user_id == admin.user.id:
                is_admin = True
                break

        if not is_admin:    # user is not admin
            bot.answer_callback_query(call.id, "Ти хто такий шоб сюда тикать? Адміна зови!!!", show_alert=True)
        else:               # user is admin
            sql_get_candidates_count = f"SELECT COUNT(*) FROM elections WHERE chatid = CAST({chat_id} AS varchar)"
            db_object.execute(sql_get_candidates_count)
            count = db_object.fetchone()

            if count is None or count[0] < 3:
                bot.answer_callback_query(call.id, "Замало кандидатів! Треба хоть 3", show_alert=True)
            else:           # start elections
                bot.send_message(chat_id, "Вибори почались!")
                self.show_candidates(call.message)
                bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    # deletes candidate from elections in DB
    def _delete_candidate_(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        chat_id = call.message.chat.id

        db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
        on_elections = db_object.fetchone()
        if on_elections is None or on_elections[0] is None:
            bot.answer_callback_query(call.id, "і шо я сука маю видалити по твоєму", show_alert=True)
        else:
            db_object.execute(f"DELETE FROM elections WHERE userid = {user_id}")
            db_connection.commit()
            self._edit_candidates_(call)
            bot.answer_callback_query(call.id, "всьо, нема тебе на виборах", show_alert=True)

    # adds candidate to elections in DB
    def _add_candidate_(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        chat_id = call.message.chat.id

        sql_get_user_info = f"SELECT level, name, username, money, rating FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_user_info)
        result = db_object.fetchone()
        sql_get_level = f"SELECT level FROM deputats JOIN elections e on deputats.userid = e.userid"
        db_object.execute(sql_get_level)
        level = db_object.fetchone()
        db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
        on_elections = db_object.fetchone()
        if on_elections is not None:
            bot.answer_callback_query(call.id, "так ти вже на виборах", show_alert=True)
        elif result is None or result[0] is None:
            bot.answer_callback_query(call.id, "кого ти блять на вибори посилаєш", show_alert=True)
        elif result[0] < 4:
            bot.answer_callback_query(call.id, "підрости", show_alert=True)
        elif result[0] == res.MAX_LEVEL:
            bot.answer_callback_query(call.id, "куда дальше, в тебе максимальний рівень", show_alert=True)
        elif result[3] < res.lvlup_requirements[result[0] - 1]:
            bot.answer_callback_query(call.id, f"Твій депутат надто бідний, для поданя кандидатури на вибори!"
                                               f"\nНеобхідно бабла:💰{res.lvlup_requirements[result[0] - 1]}$"
                                      , show_alert=True)
        elif result[4] < res.lvlup_rating[result[0] - 1]:
            bot.answer_callback_query(call.id, f"У твого депутата надто малий рейтинг серед громади!"
                                               f"\nНеобхідно рейтингу:⭐{res.lvlup_rating[result[0] - 1]}"
                                      , show_alert=True)
        elif level is not None and result[0] != level[0]:
            bot.answer_callback_query(call.id, "в тебе опше не той же рівень, шо у кандидатів", show_alert=True)
        else:   # add candidate
            db_object.execute(f"INSERT INTO elections(userid, chatid, votes) VALUES({user_id}, {chat_id}, 0)")
            db_connection.commit()
            self._edit_candidates_(call)
            bot.answer_callback_query(call.id, "єсть кантакт", show_alert=True)

    # edits election-message, adds or removes candidates from it
    def _edit_candidates_(self, call):
        db_object = self.db_object
        bot = self.bot
        chat_id = call.message.chat.id
        buttons = types.InlineKeyboardMarkup()
        buttons.add(types.InlineKeyboardButton(text="Подати свою кандидатуру", callback_data='ela'))
        buttons.add(types.InlineKeyboardButton(text="Забрати свою кандидатуру", callback_data='eld'))
        buttons.add(types.InlineKeyboardButton(text="Завершити набір кандидатів", callback_data='els'))
        sql_get_candidates = f"SELECT username, name FROM deputats JOIN elections e on deputats.userid = e.userid " \
                             f"WHERE chatid = CAST({chat_id} AS varchar)"
        db_object.execute(sql_get_candidates)
        result = db_object.fetchall()
        names = "Ініційовано початок виборів! Кандидати:"
        for resul in result:
            names += f"\n{resul[1]} ({resul[0]})"
        bot.edit_message_text(names, chat_id, call.message.message_id, reply_markup=buttons)

    def me(self, message):
        bot = self.bot
        buttons = types.InlineKeyboardMarkup()
        killed = types.InlineKeyboardButton(text='Кількість вбитих депутатів', callback_data="killed_me")
        top = types.InlineKeyboardButton(text='Топ користувачів', callback_data="top_me")
        buttons.add(killed, top)
        bot.send_message(message.chat.id, "Меню користувача",reply_markup=buttons)

    def deputat(self, message):
        bot = self.bot
        buttons = types.InlineKeyboardMarkup()
        get = types.InlineKeyboardButton(text='Получити дєпутата', callback_data="get_deputat")
        show = types.InlineKeyboardButton(text='Позирити на депутата', callback_data="show_deputat")
        work = types.InlineKeyboardButton(text='Працювати', callback_data="work_deputat")
        rating = types.InlineKeyboardButton(text='Підвищити рейтинг', callback_data="rating_deputat")
        lvlup = types.InlineKeyboardButton(text='Підвищити рівень', callback_data="lvlup_deputat")
        buttons.add(get, show, work, rating, lvlup)
        bot.send_message(message.chat.id, "Меню дєпутата", reply_markup=buttons)

    def business(self, message):
        bot = self.bot
        buttons = types.InlineKeyboardMarkup()
        visit = types.InlineKeyboardButton(text='Зібрати бабло', callback_data=f"collect_business {message.from_user.id}")
        provide = types.InlineKeyboardButton(text='Забезпечити', callback_data=f"provide_business {message.from_user.id}")
        buy = types.InlineKeyboardButton(text='Купити бізнєс', callback_data=f"buy_business")
        show = types.InlineKeyboardButton(text='Покажи', callback_data=f"show_business")
        buttons.add(visit, provide, buy, show)
        bot.send_message(message.chat.id, "Меню бізнесяк", reply_markup=buttons)

    # buy user a new business
    def buy_business_deputat(self, message):
        bot = self.bot
        if message.chat.type != "private":
            bot.reply_to(message, "Команду слід писати в ПП боту!")
        else:
            buttons = types.InlineKeyboardMarkup()
            for i in range(len(res.biz_prices)):
                buttons.add(
                    types.InlineKeyboardButton(text=res.biz_name[i] + f"💰{res.biz_prices[i]}", callback_data=f'bb{i}'))
            buttons.add(types.InlineKeyboardButton(text="І шо мені вибирати?", callback_data="help"))
            bot.reply_to(message, res.biz_text, reply_markup=buttons)

    # handle purchase call
    def handle_biz_purchase_deputat(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        sql_get_money = f"SELECT deputatid, money FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_money)
        result = db_object.fetchone()
        biz_id = int(call.data[2:3])
        biz_name = res.biz_db_name[biz_id]

        if not result or result[0] is None:     # if user doesn't have a deputat
            bot.send_message(call.message.chat.id, "І кому ти зібрався купляти? Собі чи шо?")
        elif result[1] < res.biz_prices[biz_id]:
            bot.send_message(call.message.chat.id, "Твій депутат надто бідний, шоб купити о це вот")
            bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
        else:
            sql_get_businesses = f"SELECT kid, negr, kiosk, deputatid FROM business WHERE userid = {user_id}"
            db_object.execute(sql_get_businesses)
            deputat_id = db_object.fetchone()
            if deputat_id is None:  # if user had no biz of this type, use INSERT
                sql_new_biz = f"INSERT INTO business(userid, deputatid, {biz_name}) VALUES({user_id}, {result[0]}, 1)"
                db_object.execute(sql_new_biz)
                db_connection.commit()
                self._purchase_update_(call, result, biz_id)
            else:                   # use UPDATE
                if deputat_id[biz_id] is None:
                    biz_count = 1
                else:
                    biz_count = deputat_id[biz_id] + 1
                sql_update_biz = f"UPDATE business SET {biz_name} = {biz_count}, {biz_name + 'visit'} = NULL, " \
                                 f"{biz_name + 'work'} = NULL WHERE userid = {user_id}"
                db_object.execute(sql_update_biz)
                db_connection.commit()
                self._purchase_update_(call, result, biz_id)

    # show user's businesses
    def show_business_deputat(self, message):
        db_object = self.db_object
        bot = self.bot
        user_id = message.from_user.id
        sql_get_bizs = f"SELECT kid, negr, kiosk FROM business WHERE userid = {user_id}"
        db_object.execute(sql_get_bizs)
        result = db_object.fetchone()
        if not result:
            bot.reply_to(message, "У тебе нема депутата, або бізнесів!")
        else:
            reply_text = "Бізнеси твого депутата:"
            for i in range(len(result)):
                if result[i] is not None:
                    reply_text += f"\n{res.biz_name[i]} - {result[i]}"
            bot.reply_to(message, reply_text)
            bot.send_sticker(message.chat.id, res.money_pagulich_sticker)

    # starts election's recruitment
    def elections_deputat(self, message):
        bot = self.bot
        db_object = self.db_object
        if message.chat.type == "private":
            bot.reply_to(message, "І шо блять? Ти тут один, тому сю команду в груповий чат писать надо да")
        else:
            buttons = types.InlineKeyboardMarkup()
            buttons.add(types.InlineKeyboardButton(text="Подати свою кандидатуру", callback_data='ela'))
            buttons.add(types.InlineKeyboardButton(text="Забрати свою кандидатуру", callback_data='eld'))
            buttons.add(types.InlineKeyboardButton(text="Завершити набір кандидатів", callback_data='els'))
            chat_id = message.chat.id
            sql_get_candidates = f"SELECT username, name FROM deputats JOIN elections e on deputats.userid = e.userid " \
                  f"WHERE chatid = CAST({chat_id} AS varchar)"
            db_object.execute(sql_get_candidates)
            result = db_object.fetchall()
            names = ""
            for resul in result:
                names += f"\n{resul[1]} ({resul[0]})"
            bot.reply_to(message, f"Ініційовано початок виборів! Кандидати:{names}", reply_markup=buttons)

    # handles elections (call-buttons)
    def handle_elect_deputat(self, call):  # this method handles buttons from elections_deputat method
        call_type = call.data[2:3]

        if call_type == 's':
            self._start_elections_(call)
        elif call_type == 'd':
            self._delete_candidate_(call)
        elif call_type == 'a':
            self._add_candidate_(call)

    # shows candidates in current elections
    def show_candidates(self, message):
        db_object = self.db_object
        bot = self.bot
        chat_id = message.chat.id
        sql_get_candidates = f"SELECT username, name, photo, level, money, rating, e.votes FROM deputats " \
                             f"JOIN elections e on deputats.userid = e.userid " \
                             f"WHERE chatid = CAST({chat_id} AS varchar) order by e.userid"
        db_object.execute(sql_get_candidates)
        result = db_object.fetchall()

        if result is None:  # no candidates
            bot.send_message(message.chat.id, "Каво, куда і шо...")
        else:
            i = 1
            bot.send_message(message.chat.id, "ВО ТОВО ВАШІ КАНДИДАТИ Є")
            for ress in result:
                text = str(i) + ' ' + ress[1] + ' (' + ress[0] + ') 💰' + str(ress[4]) + '$ ⭐' + str(ress[5]) + ' 📊'\
                       + str(ress[6])
                bot.send_photo(message.chat.id, res.level_photos[ress[3] - 1][ress[2]], caption=text)
                i += 1
            text = "Для голосування введіть команду /vote та номер кандидата відповідно до вище наданого списку" \
                   "\nНаприклад: /vote 3 - проголосувати за 3 кандидата"
            bot.send_message(message.chat.id, text)

    # vote for some candidate
    def election_vote(self, message):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = message.from_user.id
        chat_id = message.chat.id

        sql_get_candidates_count = f"SELECT COUNT(*) FROM elections WHERE chatid = CAST({chat_id} AS varchar)"
        db_object.execute(sql_get_candidates_count)
        count = db_object.fetchone()
        sql_get_voted = f"SELECT userid FROM voted WHERE chatid = CAST({chat_id} AS varchar) and userid = {user_id}"
        db_object.execute(sql_get_voted)
        result = db_object.fetchone()
        vote_for = int(message.text[6:])    # get number of candidate
        if count is None or vote_for <= 0 or vote_for > count[0] or result is not None:     # wrong input
            bot.send_message(message.chat.id, "Уїбати чи в'єбати?")
        else:
            vote_for -= 1
            sql_get_votes = f"SELECT votes FROM elections WHERE chatid = CAST({chat_id} AS varchar) order by userid " \
                            f"OFFSET {vote_for} LIMIT 1"
            db_object.execute(sql_get_votes)
            result = db_object.fetchone()
            votes = int(result[0]) + 1
            sql_vote = f"UPDATE elections SET votes = {votes} WHERE chatid = CAST({chat_id} AS varchar) and " \
                       f"userid = (select userid from elections order by userid offset {vote_for} limit 1)"
            db_object.execute(sql_vote)
            db_connection.commit()
            sql_update_voted = f"INSERT INTO voted(userid, chatid) VALUES {user_id, chat_id}"
            db_object.execute(sql_update_voted)
            db_connection.commit()
            bot.send_message(message.chat.id, "Голос прийнято!")

    # choose winner, lvlup
    def finish_election(self, message):
        bot = self.bot
        db_object = self.db_object
        db_connection = self.db_connection
        user_id = message.from_user.id
        chat_id = message.chat.id
        isadmin = False
        admins_t = bot.get_chat_administrators(message.chat.id)
        for admin in admins_t:
            if user_id == admin.user.id:
                isadmin = True
                break
        if not isadmin:
            bot.send_message(message.chat.id, "Ти хто такий шоб сюда тикать, сука? АДМІНА ЗОВИ!!!")
        else:
            sql_get_winner = f"SELECT elections.userid, d.level, d.username FROM elections " \
                             f"JOIN deputats d on elections.userid = d.userid " \
                             f"WHERE chatid = CAST({chat_id} AS varchar) ORDER BY votes DESC LIMIT 1"
            db_object.execute(sql_get_winner)
            result = db_object.fetchone()
            if result is None:  # if no elections are held in chat
                bot.send_message(message.chat.id, "Ну ти зовсім дебіл, чи хіба трошка?")
            else:               # lvlup winner, finish-up
                photo = random.randint(0, len(res.level_photos[result[1]]) - 1)
                sql_lvlup = f"UPDATE deputats SET level = {result[1] + 1}, photo = {photo} WHERE userid = {result[0]}"
                db_object.execute(sql_lvlup)
                db_connection.commit()
                bot.send_message(message.chat.id, f"УРА УРА УРА\nВот наш переможець туво є да - {result[2]}")
                bot.send_sticker(message.chat.id, res.happy_sticker)
                sql_clear_elections = f"DELETE FROM elections WHERE chatid = CAST({chat_id} AS varchar)"
                db_object.execute(sql_clear_elections)
                db_connection.commit()
                sql_clear_voted = f"DELETE FROM voted WHERE chatid = CAST({chat_id} AS varchar)"
                db_object.execute(sql_clear_voted)
                db_connection.commit()

    # kills user's deputat
    def kill_deputat(self, message):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = message.from_user.id
        sql_get_killed = f"SELECT deputatid, killed FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_killed)
        result = db_object.fetchone()
        if not result:
            bot.reply_to(message, "А шо вбивати то?")
        elif result[0] is None:
            bot.reply_to(message, "Себе грохнути хочеш, чи шо?")
        else:
            if result[1] is None:
                killed = 0
            else:
                killed = result[1]
            sql_update_killed = f"UPDATE deputats SET deputatid = NULL, lastworked = NULL, killed = {killed + 1}" \
                                f" WHERE userid = {user_id}"
            db_object.execute(sql_update_killed)
            db_connection.commit()
            sql_delete_business = f"DELETE FROM business WHERE userid = {user_id}"
            db_object.execute(sql_delete_business)
            db_connection.commit()
            bot.reply_to(message, "Депутату розірвало сраку...\nОтримати нового - /get")
