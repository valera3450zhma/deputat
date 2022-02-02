import res


# sends count'o killed deputats bu user
def killed_deputats(deputat, call):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id
    sql_get_killed = f"SELECT killed_deputats FROM users WHERE user_id = {user_id}"
    db_object.execute(sql_get_killed)
    result = db_object.fetchone()
    if result is None or result[0] is None:
        bot.answer_callback_query(call.id, "Ти ше не вбивав свого дєпутата", show_alert=True)
    else:
        bot.send_message(call.message.chat.id, f"Вбито депутатів: {result[0]}")


# sends top users
def top_deputat(deputat, call):
    db_object = deputat.db_object
    bot = deputat.bot
    user_id = call.from_user.id
    sql_top = f"select user_firstname, d.money from users join deputats d on users.deputat_id = d.deputat_id " \
              f"order by (d.money + (" \
              f"((select count(level) from businesses " \
              f"where level = 1 and businesses.user_id = users.user_id) * {res.biz_prices[0]})" \
              f"+((select count(level) from businesses " \
              f"where level = 2 and businesses.user_id = users.user_id) * 500)" \
              f"+((select count(level) from businesses " \
              f"where level = 3 and businesses.user_id = users.user_id) * 3000))" \
              f") DESC"
    db_object.execute(sql_top)
    result = db_object.fetchall()
    if not result:
        bot.send_message(call.message.chat.id, "Здається, ніхто навіть не має дупетата...")
    else:
        text = ''
        i = 0
        for row in result:
            if row[3] in res.SU:    # skip admins
                continue
            i += 1
            if i > 10 and row[3] != user_id:    # skip non-top-10
                continue
            text += f"{i} - {row[0]}\n💰{row[1]}$ - ⭐{row[2]}\n"
        bot.send_message(call.message.chat.id, text)
