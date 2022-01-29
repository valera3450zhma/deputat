import datetime
import random
import res
from telebot import types

# DOCUMENTATION
# Мене їбало робити нормальну документацію типу Java-Doc, тому буде таке
# Typical operations TO-DO:
# Add new level
#
#
#


class Deputat(object):
    def __init__(self, db_object, db_connection, bot):
        self.db_object = db_object
        self.db_connection = db_connection
        self.bot = bot

    # sets minimal possible id
    def _set_deputat_id(self, last_deputat):
        db_object = self.db_object
        deputat_id = -2147483648            # set minimal value for type int in PostgreSQL
        if last_deputat is not None:        # user is not first in DB
            while True:                     # run through all users and check if there is a deputat with that ID
                sql_deputat_id = f"SELECT userid FROM deputats WHERE deputatid = {deputat_id}"
                db_object.execute(sql_deputat_id)
                dep = db_object.fetchone()
                if dep is None:             # if deputat was not found
                    break                   # id is suitable, we will use it
                else:                       # else, we will try a bigger one
                    deputat_id += 1
        return deputat_id

    # commits to DB work-info, returns earned money
    def _work_(self, data, user_id):
        db_object = self.db_object
        db_connection = self.db_connection
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        earned = random.randint(10, 100) * res.money_earn_multiplier[data[1] - 1]
        db_object.execute("UPDATE deputats SET lastworked = %s, money = %s WHERE userid = %s",
                          (today_str, earned + int(data[0]), user_id))
        db_connection.commit()
        return earned

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
            bot.send_message(chat_id, "Ти хто такий шоб сюда тикать, сука? АДМІНА ЗОВИ!!!")
        else:               # user is admin
            sql_get_candidates_count = f"SELECT COUNT(*) FROM elections WHERE chatid = CAST({chat_id} AS varchar)"
            db_object.execute(sql_get_candidates_count)
            count = db_object.fetchone()

            if count is None or count[0] < 3:
                bot.send_message(chat_id, "Замало кандидатів! Мінімум 3 чибзоїда")
            else:           # start elections
                bot.send_message(chat_id, "Вибори почались!")
                self.show_candidates(call.message)
                bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

    # deletes candidate from elections in DB
    def _delete_candidate_(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.message.from_user.id
        chat_id = call.message.chat.id

        db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
        result = db_object.fetchone()
        if result is None:
            bot.send_message(chat_id, "я тут хочу вкидувати алер а не повідомлення")
        else:
            db_object.execute(f"DELETE FROM elections WHERE userid = {user_id}")
            db_connection.commit()
            self._edit_candidates_(call)
            bot.send_message(chat_id, "Вашу кандідатуру видалено!")

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
        if result is None or result[0] is None:
            bot.send_message(chat_id, "У вас нема депутата!")
        elif result[0] < 4:
            bot.send_message(chat_id, "У вас замалий рівень для подання кандидатури!")
        elif result[3] < res.lvlup_requirements[result[0] - 1]:
            bot.send_message(chat_id, f"Твій депутат надто бідний, для поданя кандидатури на вибори!\nНеобхідно бабла:"
                                      f"💰{res.lvlup_requirements[result[0] - 1]}$")
        elif result[4] < res.lvlup_rating[result[0] - 1]:
            bot.send_message(chat_id, f"У твого депутата надто малий рейтинг серед громади!\nНеобхідно рейтингу:"
                                      f"⭐{res.lvlup_rating[result[0] - 1]}")
        elif level is not None and result[0] != level[0]:
            bot.send_message(chat_id, "У вас опше не той рівень шо у кандидатів!")
        elif result[0] == res.MAX_LEVEL:
            bot.send_message(chat_id, "У вашого депутата максимальний рівень!")
        else:   # add candidate
            db_object.execute(f"SELECT userid FROM elections WHERE userid = {user_id}")
            result = db_object.fetchone()
            if result is not None:
                bot.send_message(chat_id, "Ваша кандидатура вже на виборах!")
            else:
                db_object.execute(f"INSERT INTO elections(userid, chatid, votes) VALUES({user_id}, {chat_id}, 0)")
                db_connection.commit()
                self._edit_candidates_(call)

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

    # set buttons with businesses names
    def _create_business_buttons_(self, message, price, modifier):
        db_object = self.db_object
        bot = self.bot
        user_id = message.from_user.id
        sql_get_businesses = f"SELECT kid, negr, kiosk FROM business WHERE userid = {user_id}"
        db_object.execute(sql_get_businesses)
        result = db_object.fetchone()

        if result is None:
            bot.reply_to(message, "Бізнесів не знайдено!")
            bot.send_sticker(message.chat.id, res.sad_sticker)
        else:
            buttons = types.InlineKeyboardMarkup()
            for i in range(len(res.biz_prices)):
                if result[i] is not None:
                    buttons.add(types.InlineKeyboardButton
                                (text=res.biz_provide_buttons(result, i, price), callback_data=f'{modifier}{i}'))
            bot.reply_to(message, res.biz_text, reply_markup=buttons)

    # commit biz purchase to DB
    def _purchase_update_(self, call, result, biz_id):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        sql_update_money = f"UPDATE deputats SET money = {result[1] - res.biz_prices[biz_id]} WHERE userid = {user_id}"
        db_object.execute(sql_update_money)
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_photos[biz_id],
                       caption=f"Ви успішно купили \"{res.biz_name[biz_id]}\"!")
        if random.randint(0, 4) == 0:
            sql_get_rating = f"SELECT rating FROM deputats WHERE userid = {user_id}"
            db_object.execute(sql_get_rating)
            result = db_object.fetchone()
            sql_update_rating = f"UPDATE deputats SET rating = {result[0] - res.biz_rating_drop[biz_id]} " \
                                f"WHERE userid = {user_id}"
            db_object.execute(sql_update_rating)
            db_connection.commit()
            bot.send_photo(call.message.chat.id, res.biz_rating_photo[biz_id], caption=res.biz_rating_text[biz_id])

    # gives user a deputat
    def get_deputat(self, message):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = message.from_user.id

        sql_user_info = f"SELECT userid, deputatid FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_user_info)
        result = db_object.fetchone()

        db_object.execute("SELECT deputatid FROM deputats WHERE deputatid IS NOT NULL ORDER BY deputatid DESC LIMIT 1")
        last_deputat = db_object.fetchone()

        if result is None:  # user is not registered, use INSERT
            deputat_id = self._set_deputat_id(last_deputat)
            sql_new_user = f"INSERT INTO deputats(userid, money, name, level, photo, username, deputatid, rating)" \
                           f" VALUES( {user_id}, {random.randint(10, 100)}, {random.choice(res.deputatNames)}, {1}," \
                           f" {random.randint(0, len(res.level_photos[0]) - 1)}, {message.from_user.first_name}," \
                           f" {deputat_id}, {0})"
            db_object.execute(sql_new_user)
            db_connection.commit()
            bot.reply_to(message, "Осьо! Ваш перший дєпутат! Позирити на нього - /show")

        elif result[1] is None:     # user doesn't have a deputat, use UPDATE
            deputat_id = self._set_deputat_id(last_deputat)
            sql_new_deputat = f"UPDATE deputats SET deputatid = {deputat_id}, money = {random.randint(10, 100)}, " \
                              f"name = {random.choice(res.deputatNames)}, level = %s,  photo = %s, rating = %s " \
                              f"WHERE userid = %s", (1, random.randint(0, len(res.level_photos[0]) - 1), 0, result[0])
            db_object.execute(sql_new_deputat)
            db_connection.commit()
            bot.reply_to(message, "Гля який! Депута-а-а-атіще! Глянуть на підарасіка - /show")
        else:
            bot.reply_to(message, "В тебе вже є депутат")
            bot.send_sticker(message.chat.id, res.what_sticker)

    # show info about user's deputat
    def show_deputat(self, message):
        db_object = self.db_object
        bot = self.bot
        user_id = message.from_user.id
        sql_get_user_info = f"SELECT name, money, level, photo, deputatid, rating FROM deputats " \
                            f"WHERE deputats.userid = {user_id}"
        db_object.execute(sql_get_user_info)
        result = db_object.fetchone()

        if not result or result[4] is None:     # if user is not in DB or user doesn't have a deputat
            bot.reply_to(message, "Ніхуя нема...")
        else:                                   # user has deputat, show info
            deputat_photo = res.level_photos[result[2] - 1][result[3]]
            reply_message = f"👨🏻 Ім'я: {result[0]}\n💰 Бабло: ${result[1]}\n⭐️ Рейтинг: {result[5]}" \
                            f"\n📚 Рівень: {result[2]} - {res.level_captions[result[2] - 1]} "
            bot.send_photo(message.chat.id, deputat_photo, reply_to_message_id=message.id, caption=reply_message)

    # makes user's deputat work
    def work_deputat(self, message):
        db_object = self.db_object
        bot = self.bot
        user_id = message.from_user.id

        sql_last_worked = f"SELECT lastworked FROM deputats WHERE deputats.userid = {user_id}"
        db_object.execute(sql_last_worked)
        last_worked = db_object.fetchone()
        sql_get_user_info = f"SELECT money, level, name, deputatid FROM deputats WHERE deputats.userid = {user_id}"
        db_object.execute(sql_get_user_info)
        data = db_object.fetchone()

        if not last_worked or data[3] is None:
            bot.reply_to(message, "В тебе нема депутата, шоб він працював")
        elif not last_worked[0]:            # if works first time ever
            earned = self._work_(data, user_id)
            bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                           caption=f"{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}",
                           reply_to_message_id=message.id)
        else:                               # if worked earlier
            worked = datetime.date(last_worked[0].year, last_worked[0].month, last_worked[0].day)
            today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
            if (today - worked).days >= 1:  # didn't work in a day
                earned = self._work_(data, user_id)
                bot.send_photo(message.chat.id, res.work_photos[data[1] - 1],
                               caption=f"{data[2]}{res.work_text[data[1] - 1]}\n💰 Дохід: ${earned}")
            else:                           # if worked today
                bot.send_photo(message.chat.id, random.choice(res.not_working_photos),
                               caption="Твій депутат вже заїбався бо нині відхуячив своє",
                               reply_to_message_id=message.id)

    # level-ups deputat
    def lvlup_deputat(self, message):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = message.from_user.id

        sql_get_user_info = f"SELECT level, money, deputatid, rating FROM deputats WHERE deputats.userid = {user_id}"
        db_object.execute(sql_get_user_info)
        result = db_object.fetchone()

        if not result or result[2] is None:     # deputat was not found
            bot.reply_to(message, "А шо апати то?")
        elif result[0] >= 4:                    # level too high to lvlup
            bot.reply_to(message, "Для підвищення рівня, необхідно ініціювати вибори!")
        elif result[1] < res.lvlup_requirements[result[0] - 1]:     # not enough money
            bot.reply_to(message, f"Твій депутат надто бідний, щоб перейти на новий рівень!"
                                  f"\n💰 Необхідно грошей: ${res.lvlup_requirements[result[0] - 1]}")
            bot.send_sticker(message.chat.id, res.sad_sticker)
        elif result[3] < res.lvlup_rating[result[0] - 1]:           # not enough rating
            bot.reply_to(message, f"У твого депутата надто низький рейтинг, щоб перейти на новий рівень!"
                                  f"\n⭐ Необхідно рейтингу: {res.lvlup_rating[result[0] - 1]}")
            bot.send_sticker(message.chat.id, res.sad_sticker)
        else:                                   # deputat will lvlup
            sql_lvlup = f"UPDATE deputats SET level = {result[0] + 1}," \
                        f" photo = {random.randint(0, len(res.level_photos[result[0]]) - 1)}," \
                        f" lastworked = NULL, money = {result[1] - res.lvlup_requirements[result[0] - 1]} " \
                        f"WHERE userid = {user_id}"
            db_object.execute(sql_lvlup)
            db_connection.commit()
            bot.reply_to(message, "Депутата підвищено до нового рівня! - /show")
            bot.send_sticker(message.chat.id, res.happy_sticker)

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
            db_object.execute(
                f"SELECT username, name FROM deputats JOIN elections e on deputats.userid = e.userid "
                f"WHERE chatid = CAST({chat_id} AS varchar)")
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

    # visit user's business
    def visit_business_deputat(self, message):
        bot = self.bot
        if message.chat.type != "private":
            bot.reply_to(message, "Команду слід писати в ПП боту!")
        else:
            self._create_business_buttons_(message, False, "vb")

    # handle's callback
    def handle_visit_business_deputat(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        biz_id = int(call.data[2:3])
        biz_name = res.biz_db_name[biz_id]
        biz_work = biz_name + 'work'
        biz_visit = biz_name + 'visit'

        sql_get_businesses = f"SELECT deputatid, {biz_name}, {biz_visit}, {biz_work} FROM business " \
                             f"WHERE userid = {user_id}"
        db_object.execute(sql_get_businesses)
        result = db_object.fetchone()
        sql_get_money = f"SELECT money FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_money)
        money = db_object.fetchone()
        deputat_id = result[0]
        biz_count = result[1]
        visited = result[2] if result[2] is not None else datetime.date.min
        worked = result[3] if result[3] is not None else datetime.date.min
        today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)

        if not result or deputat_id is None or biz_count is None:
            bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
        elif (today - worked).days < 1:     # business worked today
            bot.send_message(call.message.chat.id, res.biz_worked_text[biz_id])
        elif (today - visited).days >= 7:   # business was not suplied in 7 days
            bot.send_message(call.message.chat.id, res.biz_not_visited_text[biz_id])
        else:                               # collect money from business
            earned = res.biz_profits[biz_id] * random.randint(1, 10) * biz_count
            sql_update_money = f"UPDATE deputats SET money = {money[0] + earned} WHERE userid = {user_id}"
            db_object.execute(sql_update_money)
            db_connection.commit()
            today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
            sql_update_biz_worked = f"UPDATE business SET {biz_work} = %s WHERE userid=%s", (today_str, user_id)
            db_object.execute(sql_update_biz_worked)
            db_connection.commit()
            bot.send_photo(call.message.chat.id, res.biz_photos[biz_id],
                           caption=res.biz_work_text[biz_id] + str(earned))

    # supply business
    def provide_business_deputat(self, message):
        bot = self.bot
        if message.chat.type != "private":
            bot.reply_to(message, "Команду слід писати в ПП боту!")
            return
        self._create_business_buttons_(message, True, "pb")

    # handles callback
    def handle_provide_business_deputat(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        biz_id = int(call.data[2:3])
        biz_name = res.biz_db_name[biz_id]
        biz_visit = biz_name + 'visit'

        sql_get_business = f"SELECT deputatid, {biz_name}, {biz_visit} FROM business WHERE userid = {user_id}"
        db_object.execute(sql_get_business)
        result = db_object.fetchone()
        sql_get_money = f"SELECT money FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_money)
        money = db_object.fetchone()
        deputat_id = result[0]
        biz_count = result[1]
        visited = result[2] if result[2] is not None else datetime.date.min
        today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
        days_diff = (today - visited).days

        if not result or deputat_id is None or biz_count is None:
            bot.send_message(call.message.chat.id, "І кого ти провідуєш? Мать свою чи шо?")
        elif visited is not None and days_diff < 7:
            bot.send_message(call.message.chat.id,
                             f"Бізнес не потребує забезпечення, приходьте за {7 - days_diff} дні(-в)")
        elif money[0] < res.biz_provides[biz_id] * biz_count:
            bot.send_message(call.message.chat.id, "В твого депутата замало грошей для підтримання цього бізнесу!")
            bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
        else:   # supply business
            db_object.execute("UPDATE deputats SET money = %s WHERE userid = %s",
                              (money[0] - res.biz_provides[biz_id] * biz_count, user_id))
            db_connection.commit()
            today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
            db_object.execute(f"UPDATE business SET {biz_visit} = %s WHERE userid=%s", (today_str, user_id))
            db_connection.commit()
            bot.send_photo(call.message.chat.id, res.biz_provide_photos[biz_id], caption=res.biz_provide_text[biz_id])

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

    # upgrade user's rating
    def up_rating_deputat(self, message):
        bot = self.bot
        if message.chat.type != "private":
            bot.reply_to(message, "Команду слід писати в ПП боту!")
        else:
            buttons = types.InlineKeyboardMarkup()
            for i in range(len(res.rating_name)):
                buttons.add(types.InlineKeyboardButton
                            (text=res.rating_name[i] + ' $' + str(res.rating_price[i]), callback_data=f'rt{i}'))
            bot.reply_to(message, "Доступні види підняття рейтингу:", reply_markup=buttons)

    # rating upgrade handler
    def handle_rating_deputat(self, call):
        db_object = self.db_object
        db_connection = self.db_connection
        bot = self.bot
        user_id = call.from_user.id
        rating = int(call.data[2:3])
        sql_get_user_info = f"SELECT money, rating, deputatid FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_user_info)
        result = db_object.fetchone()

        if result is None or result[2] is None:     # if user doesn't have a deputat
            bot.send_message(call.message.chat.id, "У тебе немає депутата")
        elif result[0] < res.rating_price[rating]:  # if user doesn't have enough money
            bot.send_message(call.message.chat.id, "Твоєму депутату не вистачає грошей для цього!")
            bot.send_sticker(call.message.chat.id, res.sad_sticker)
        else:                                       # upgrade rating
            sql_update_rating = f"UPDATE deputats SET rating = {result[1] + res.rating_up[rating]} " \
                                f"WHERE userid = {user_id}"
            db_object.execute(sql_update_rating)
            db_connection.commit()
            sql_update_money = f"UPDATE deputats SET money = {result[0] - res.rating_price[rating]} " \
                               f"WHERE userid = {user_id}"
            db_object.execute(sql_update_money)
            db_connection.commit()
            bot.send_message(call.message.chat.id, f"Рейтинг серед громади піднято на {res.rating_up[rating]}⭐️")

    # sends top users
    def top_deputat(self, message):
        db_object = self.db_object
        bot = self.bot
        sql_top = "SELECT username, money, rating FROM deputats" \
                  " FULL JOIN business b on deputats.deputatid = b.deputatid" \
                  " ORDER BY (money + COALESCE(b.kid*100, 0) + COALESCE(b.negr*500, 0) + COALESCE(b.kiosk*3000, 0))" \
                  " DESC LIMIT 30;"
        db_object.execute(sql_top)
        result = db_object.fetchall()
        if not result:
            bot.reply_to(message, "Здається, ніхто навіть не має дупетата...")
        else:
            text = ''
            i = 1
            for row in result:
                text += f"{i} - {row[0]}\n💰{row[1]}$ - ⭐{row[2]}\n"
                i += 1
            bot.reply_to(message, text)

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
            sql_delete_business = "DELETE FROM business WHERE userid = %s", [user_id]
            db_object.execute(sql_delete_business)
            db_connection.commit()
            bot.reply_to(message, "Депутату розірвало сраку...\nОтримати нового - /get")

    # sends count'o killed deputats bu user
    def killed_deputats(self, message):
        db_object = self.db_object
        bot = self.bot
        user_id = message.from_user.id
        sql_get_killed = f"SELECT killed FROM deputats WHERE userid = {user_id}"
        db_object.execute(sql_get_killed)
        result = db_object.fetchone()
        if result is None or result[0] is None:
            bot.reply_to(message, "Ти ще не вбивав своїх депутатів")
        else:
            bot.reply_to(message, f"Вбито депутатів: {result[0]}")
