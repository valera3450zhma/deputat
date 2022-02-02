import res
import datetime
import random
from telebot import types


def _get_businesses_(db_object, user_id):
    lvls = []
    for i in range(len(res.biz_prices)):
        sql_get_businesses = f"SELECT count(level) FROM businesses WHERE user_id = {user_id} and level = {i+1};"
        db_object.execute(sql_get_businesses)
        lvls.append(db_object.fetchone())
    return lvls


# set buttons with businesses names
def _create_business_buttons_(deputat, call, price, modifier):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id
    lvls = _get_businesses_(db_object, user_id)
    has_business = False
    for lvl in lvls:
        if lvl is not None:
            has_business = True
            break
    if has_business is False:
        bot.answer_callback_query(call.id, "У тебе нема бізнесів", show_alert=True)
    else:
        buttons = types.InlineKeyboardMarkup()
        for i in range(len(res.biz_prices)):
            if lvls[i] is not None:
                buttons.add(types.InlineKeyboardButton
                            (text=res.biz_provide_buttons(lvls, i, price), callback_data=f'{modifier}{i}'))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.edit_message_text("Меню дєпутата", call.message.chat.id, call.message.message_id)


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
        if (today - last_worked).days > 1 and (today-last_provided) < 7:
            can_work += 1
        elif (today - last_worked).days < 1:
            have_worked += 1
        elif (today - last_provided) >= 7:
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
        sql_update_money = f"UPDATE deputats SET money = {money[0] + earned} WHERE user_id = {user_id}"
        db_object.execute(sql_update_money)
        db_connection.commit()
        today_str = (datetime.datetime.today() + datetime.timedelta(hours=res.hour_adjust)).strftime("%Y/%m/%d")
        sql_update_biz_worked = f"UPDATE businesses SET last_worked = '{today_str}' WHERE user_id = {user_id} " \
                                f"and level = {biz_id+1}"
        db_object.execute(sql_update_biz_worked)
        db_connection.commit()
        bot.send_photo(call.message.chat.id, res.biz_photos[biz_id],
                       caption=res.biz_work_text[biz_id] + str(earned))


def provide_business(deputat, call):
    _create_business_buttons_(deputat, call, False, "pb")


def handle_provide_business(deputat, call):
    db_object = deputat.db_object
    db_connection = deputat.db_connection
    bot = deputat.bot
    user_id = call.from_user.id
    biz_id = int(call.data[2:3])
    biz_name = res.biz_db_name[biz_id]
    biz_visit = biz_name + 'visit'

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

