import res
import datetime
import random
from telebot import types


# sets minimal possible id
def _set_business_id(deputat, last_biz):
    db_object = deputat.db_object
    biz_id = -9223372036854775808       # set minimal value for type int in PostgreSQL
    if last_biz is not None:    # user is not first in DB
        while True:                 # run through all users and check if there is a deputat with that ID
            sql_deputat_id = f"SELECT biz_id FROM businesses WHERE biz_id = {biz_id}"
            db_object.execute(sql_deputat_id)
            dep = db_object.fetchone()
            if dep is None:         # if deputat was not found
                break               # id is suitable, we will use it
            else:                   # else, we will try a bigger one
                biz_id += 1
    return biz_id


def _get_businesses_(db_object, user_id):
    lvls = []
    for i in range(len(res.biz_prices)):
        sql_get_businesses = f"SELECT count(level) FROM businesses WHERE user_id = {user_id} and level = {i+1};"
        db_object.execute(sql_get_businesses)
        result = db_object.fetchone()
        lvls.append(result[0])
    return lvls


# set buttons with businesses names
def _create_business_buttons_(deputat, call, price, modifier):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id
    lvls = _get_businesses_(db_object, user_id)

    if len(lvls) == 0:
        bot.answer_callback_query(call.id, "У тебе нема бізнесів", show_alert=True)
    else:
        buttons = types.InlineKeyboardMarkup()
        for i in range(len(res.biz_prices)):
            if lvls[i] != 0:
                buttons.add(types.InlineKeyboardButton
                            (text=res.biz_provide_buttons(lvls, i, price), callback_data=f'{modifier}{i}'))
        buttons.add((types.InlineKeyboardButton(text="Назад", callback_data="business_menu")))
        bot.edit_message_text("Меню дєпутата", call.message.chat.id, call.message.message_id, reply_markup=buttons)


# commit biz purchase to DB
def _purchase_update_(deputat, call, deput, biz_lvl):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    sql_update_money = f"UPDATE deputats SET money = {deput[0] - res.biz_prices[biz_lvl]} WHERE user_id = {user_id}"
    db_object.execute(sql_update_money)
    db_connection.commit()
    bot.send_photo(call.message.chat.id, res.biz_photos[biz_lvl],
                   caption=f"Ви успішно купили \"{res.biz_name[biz_lvl]}\"!")
    if random.randint(0, 4) == 0:
        sql_update_rating = f"UPDATE deputats SET rating = {deput[1] - res.biz_rating_drop[biz_lvl]} " \
                            f"WHERE user_id = {user_id}"
        db_object.execute(sql_update_rating)
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_rating_photo[biz_lvl], caption=res.biz_rating_text[biz_lvl])


# collects money from business
def collect_business(deputat, call):
    _create_business_buttons_(deputat, call, False, "cb")


# processes money collect for some business
def handle_collect_business(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    biz_id = int(call.data[2:3])

    sql_get_businesses = f"SELECT last_worked, last_provided FROM businesses WHERE user_id = {user_id} and level = {biz_id + 1}"
    db_object.execute(sql_get_businesses)
    user_businesses = db_object.fetchall()
    sql_biz_count = f"SELECT count(*) FROM businesses WHERE user_id = {user_id} and level = {biz_id + 1}"
    db_object.execute(sql_biz_count)
    biz_count_ = db_object.fetchall()
    sql_get_money = f"SELECT money FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_get_money)
    deput = db_object.fetchone()
    money = deput[0]
    biz_count = biz_count_[0]

    can_work = 0
    have_worked = 0
    not_supplied = 0
    today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
    for biz in user_businesses:
        last_provided = biz[1] if biz[1] is not None else datetime.date.min
        last_worked = biz[0] if biz[0] is not None else datetime.date.min
        if (today - last_worked).days > 1 and (today-last_provided).days < 7:
            can_work += 1
        if (today - last_worked).days < 1:
            have_worked += 1
        if (today - last_provided).days >= 7:
            not_supplied += 1

    if biz_count == 0:
        bot.answer_callback_query(call.id, "Чел, це піздєц, якшо ти це бачиш - швидко пиши мені в пп, бо то є БАГ!!!!",
                                  show_alert=True)
    elif have_worked == biz_count:      # business worked today
        bot.answer_callback_query(call.id, res.biz_worked_text[biz_id], show_alert=True)
    elif not_supplied == biz_count:     # business was not suplied in 7 days
        bot.answer_callback_query(call.id, res.biz_not_visited_text[biz_id], show_alert=True)
    else:                               # collect money from business
        earned = res.biz_profits[biz_id] * random.randint(3, 8) * can_work
        sql_update_money = f"UPDATE deputats SET money = {money + earned} WHERE user_id = {user_id}"
        db_object.execute(sql_update_money)
        db_connection.commit()
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        sql_update_biz_worked = f"UPDATE businesses SET last_worked = '{today_str}' WHERE user_id = {user_id} " \
                                f"and level = {biz_id+1}"
        db_object.execute(sql_update_biz_worked)
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_photos[biz_id],
                       caption=res.biz_work_text[biz_id] + str(earned))


# provides biz with resources
def provide_business(deputat, call):
    _create_business_buttons_(deputat, call, False, "pb")


# processes biz providing
def handle_provide_business(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    biz_id = int(call.data[2:3])

    sql_get_business = f"SELECT level, last_provided FROM businesses WHERE user_id = {user_id} and level = {biz_id + 1}"
    db_object.execute(sql_get_business)
    user_business = db_object.fetchone()
    sql_biz_count = f"SELECT count(*) FROM businesses WHERE user_id = {user_id} and level = {biz_id + 1}"
    db_object.execute(sql_biz_count)
    biz_count_ = db_object.fetchall()
    sql_get_money = f"SELECT money FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_get_money)
    money = db_object.fetchone()

    biz_count = biz_count_[0]
    must_be_supplied = 0
    today = datetime.date.today() + datetime.timedelta(hours=res.hour_adjust)
    for biz in user_business:
        if (today - biz[1]).days >= 7:
            must_be_supplied += 1

    if biz_count == 0:
        bot.answer_callback_query(call.id, "Чел, це піздєц, якшо ти це бачиш - швидко пиши мені в пп, бо то є БАГ!!!!",
                                  show_alert=True)
    elif must_be_supplied == 0:
        bot.answer_callback_query(call.id, f"Бізнеси не потребують забезпечення", show_alert=True)
    elif money[0] < res.biz_provides[biz_id] * must_be_supplied:
        bot.send_message(call.message.chat.id, "В твого депутата замало грошей для підтримання цього бізнесу!")
        bot.send_sticker(call.message.chat.id, res.money_valakas_sticker)
    else:  # supply business
        sql_update_money = f"UPDATE deputats SET money = {money[0] - res.biz_provides[biz_id] * biz_count} " \
                           f"WHERE user_id = {user_id}"
        db_object.execute(sql_update_money)
        db_connection.commit()
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        sql_update_provided = f"UPDATE businesses SET last_provided = '{today_str}' WHERE user_id={user_id} and level = {biz_id + 1}"
        db_object.execute(sql_update_provided)
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_provide_photos[biz_id], caption=res.biz_provide_text[biz_id])


def buy_business(deputat, call):
    bot = deputat.bot
    buttons = types.InlineKeyboardMarkup()
    for i in range(len(res.biz_prices)):
        buttons.add(types.InlineKeyboardButton(text=f'{res.biz_name[i]} - 💰{res.biz_prices[i]} $', callback_data=f'bb{i}'))
    buttons.add(types.InlineKeyboardButton(text="І шо мені вибирати?", callback_data="help"))
    buttons.add((types.InlineKeyboardButton(text="Назад", callback_data="business_menu")))
    bot.edit_message_text("Во туво купит можеш да", call.message.chat.id, call.message.message_id, reply_markup=buttons)


def handle_buy_business(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    sql_get_money = f"SELECT money, rating FROM deputats WHERE user_id = {user_id}"
    db_object.execute(sql_get_money)
    deput = db_object.fetchone()
    biz_lvl = int(call.data[2:3])

    if deput is None:  # if user doesn't have a deputat
        bot.answer_callback_query(call.id, "І кому ти зібрався купляти? Собі чи шо?")
    elif deput[0] < res.biz_prices[biz_lvl]:
        bot.answer_callback_query(call.message.chat.id, "Твій депутат надто бідний, шоб купити о це вот")
    else:
        sql_bizs = f"SELECT level FROM businesses"
        db_object.execute(sql_bizs)
        bizs = db_object.fetchone()
        business_id = _set_business_id(deputat, bizs)
        sql_new_business = f"INSERT INTO businesses(biz_id, user_id, level, last_worked, last_provided) VALUES({business_id}, {user_id}, {biz_lvl+1}, Null, Null)"
        db_object.execute(sql_new_business)
        db_connection.commit()
        _purchase_update_(deputat, call, deput, biz_lvl)



def handle_business_menu(deputat, call):
    bot = deputat.bot
    buttons = types.InlineKeyboardMarkup()
    visit = types.InlineKeyboardButton(text='Зібрати бабло', callback_data="collect_business")
    provide = types.InlineKeyboardButton(text='Забезпечити', callback_data="provide_business")
    buy = types.InlineKeyboardButton(text='Купити бізнєс', callback_data="buy_business")
    show = types.InlineKeyboardButton(text='Покажи', callback_data="show_business")
    buttons.add(visit, provide, buy, show)
    bot.edit_message_text("Меню бізнєся", call.message.chat.id, call.message.message_id, reply_markup=buttons)
