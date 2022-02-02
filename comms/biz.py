import res
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


def handle_collect_business(deputat, call):
    pass
