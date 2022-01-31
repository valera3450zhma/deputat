MAX_LEVEL = 6

hour_adjust = 2

SU = [
    506126580,
    507028811,
    376120805
]

deputatNames = [
    'Ігор',
    'Андрюха',
    'Бодя',
    'Вадім',
    'Ваня',
    'Вася',
    'Вова',
    'Вєталь',
    'Денчик',
    'Дімас',
    'Едік',
    'Женя',
    'Коля',
    'Льоша',
    'Максімка',
    'Місько',
    'Олежик',
    'Паша',
    'Петя',
    'Ромко',
    'Саня',
    'Святік',
    'Стьопа',
    'Сєрий',
    'Тьома',
    'Юлік',
    'Юрчик',
    'Ярік'
]

level_photos = [
    [
      "AgACAgIAAxkBAAIHeGHj9mhbpTDw_3j8AWOX_KupsqtTAAIPujEb2msgSzJIB7-h-csJAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHeWHj9mheyYb0EPQefPkBqCVPIP9sAAIRujEb2msgS-GUS6mFHo7UAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHemHj9mhLdoSVaQABLk8L2x8herHbFAACELoxG9prIEsVIHtaBWKgewEAAwIAA3kAAyME",
      "AgACAgIAAxkBAAIHe2Hj9mhXRdzHhsRRoJfjzDEk0NUbAAISujEb2msgS8TteNIkMn_JAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHfGHj9mhtxvpL4ENwsmMtbHgC4EAEAAITujEb2msgS-i33hSX2-rPAQADAgADeAADIwQ",
      "AgACAgIAAxkBAAIHfWHj9mgEwjZ0UKQYsiMBDKzmu13sAAIUujEb2msgS-gvclifMgsYAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHfmHj9mh-kBFsjwT1QOmHz4z3wiNfAAIVujEb2msgS6tzWfTOn5FVAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHf2Hj9mhrJyI0IFY901XHs-wsZYhcAAIWujEb2msgS_IC1GY0FQG4AQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHgGHj9mgyYK-Hl9KPRtlRKdWmXVNDAAIXujEb2msgS8OG3tSm1YJzAQADAgADeQADIwQ",
      "AgACAgIAAxkBAAIHgWHj9mjaRy6PO0J5Lmpq-SKSZCaMAAIYujEb2msgS7p82Yhd9HRfAQADAgADeQADIwQ"
    ],
    [
        "AgACAgIAAxkBAAIDimHhgF6T-i4tut4lphGrTQK8j3JyAALQtjEbJ_8QS9aX-uF4-rZUAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDi2HhgF6LVlI0xUV3RHhSWmTBkmFFAAKSuTEbmVIRS-PN1nulOCtzAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDjGHhgF5hNB1q0xGGCJFfrEsMeUxKAAKTuTEbmVIRS5Jh94egW-2aAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDjWHhgF6DVSOB5vAPSzRS3SVDmAXYAAKUuTEbmVIRS977waYXPdB6AQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDjmHhgF6OcXCId0dWdajhnhYcSz3KAAKVuTEbmVIRSyVOYn4OwluQAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDj2HhgF4n-rPihRnAMsje2-huB1TtAAKWuTEbmVIRS-K2ofH5QRZ-AQADAgADbQADIwQ",
        "AgACAgIAAxkBAAIDkGHhgF7mezDUsPsSE3081a6j5-w3AAKXuTEbmVIRS7R_2UR8FdctAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDkWHhgF4KvsyK4KYri3pZ6j-5r8pjAAKYuTEbmVIRS3kz38mQVmhmAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDkmHhgF4MPaUNwxlVhgvsb3_Vn0rZAAKZuTEbmVIRS_8lxJ6NF4CaAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIDk2HhgF5PRAkVxgnedMhAGuC2yt5aAAKauTEbmVIRSxN7rNAUMoUDAQADAgADeAADIwQ"
    ],
    [
        "AgACAgIAAxkBAAIPe2Hr-QY3AYEuMzAKqxweh9ga13w1AAKiuDEbTFVhSxNSx2xbzUqJAQADAgADbQADIwQ",
        "AgACAgIAAxkBAAIPfWHr-Q0QQTI8U8IrfWEGVTGaSi_UAAKjuDEbTFVhS663dCwElSAYAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIPf2Hr-RQo-T1EYfxA2bH3X7y0YhlFAAKkuDEbTFVhS1WhVkm5RzMHAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIPgWHr-TH1DVi_X12gJYidsRlAZRIFAAKluDEbTFVhS4Os9shmbgFeAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIPg2Hr-UYd8LMawVvwCaBP5bFBvmKzAAKmuDEbTFVhS8bIVn9NYvwMAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIPhWHr-VFMggGiUAnfxIOzWDJLp6ZmAAKnuDEbTFVhSzbpaoSFrp5NAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIPh2Hr-VlBxywdptGlGp4Oy8e9C1MZAAKouDEbTFVhS2ZBpGyb8ygMAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIPiWHr-a4gY-hhvWMRodhIyqYQOONpAAKpuDEbTFVhSxzAoJ-498DDAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIPi2Hr-cSwxGyZn_--xmgDOrb-QBUWAAKquDEbTFVhS6o3mpl_oLPgAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIPjWHr-dODKwbKPi9Bw7lwuoSdE_MbAAKruDEbTFVhS6O3Tv-f9CuQAQADAgADbQADIwQ"
    ],
    [
        "AgACAgIAAxkBAAIDnmHhgMjHO6ORGcPbOK9NBCP8aOsBAAJTvDEbRTsJS3Ic8acDtj4vAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDn2HhgMjrRfTsxFgjly0O0EfHav20AAJUvDEbRTsJS892LhLAQ6iiAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDoGHhgMi9su9PfcropFTfAbE-ms03AAJWvDEbRTsJS6SeFyIjJppkAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDoWHhgMgmNpGLCDjCfxSnm6qTKw05AAJVvDEbRTsJSxSkp_5t1TikAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDomHhgMjcBEHk978CX_ucHXNG8H2pAAJXvDEbRTsJS6tqQQ89-LzRAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDo2HhgMiOJWBG3g936sH68hvb4_4dAAJYvDEbRTsJS9xQutzjw6SKAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDpGHhgMhgIKl3ElMc4kY9ioEHXGC5AAJavDEbRTsJS4xW-aa6oik8AQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDpWHhgMgbo2gJx7GS6BxBzOUD15XXAAJZvDEbRTsJSxDh2kfKhfxkAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDpmHhgMgiXlRQe3Z4d3C8TAthtz2FAAJbvDEbRTsJS3g1TjCtZ0SMAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIDp2HhgMjFHTsSUMlge4xUvk-TR7IiAAJcvDEbRTsJS-ROU_wXNquFAQADAgADeQADIwQ"
    ],
    [
        "AgACAgIAAxkBAAIQ32Huu-XJbcJp7y2qlQ_K12ws-Um7AALstzEbuAF5S3Z1BxN0mqbbAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIQ4WHuu-1RBZHKtztMNoCyHB5WDx-sAALttzEbuAF5Sw_xFlm9PkEtAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIQ42Huu_dJRAlwHOa5hR1w2KU6k4fsAALwtzEbuAF5S0ROe_jxoS_1AQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIQ5WHuvAWgKzN57B1wepr-5TByTvbTAALxtzEbuAF5S7OyTcUAAYoXNgEAAwIAA3kAAyME",
        "AgACAgIAAxkBAAIQ52HuvCOr_sQVz1_BVDo1E7nwd7XnAALytzEbuAF5S-y1aHt6xOQ5AQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIQ6WHuvDJDVp4xnK15F2ohK4MR5PskAALztzEbuAF5S6mFGfwihkWkAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAIQ62HuvD31PDlG4DWBSmZIcswwqX4kAAL0tzEbuAF5S3j4xZ1ShMDVAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIQ7WHuvEyjqhGVODPHozgKDxLp-kccAAL2tzEbuAF5S2Noh30oZMsfAQADAgADbQADIwQ",
        "AgACAgIAAxkBAAIQ72HuvHUhmH_g6stfVzjzBMUKzXY5AAL3tzEbuAF5S9ng2LmGhblHAQADAgADbQADIwQ",
        "AgACAgIAAxkBAAIQ8WHuvJOwBJ58sgwwoH3D9dk2l5d3AAL4tzEbuAF5S4QsmCLfxdY3AQADAgADeAADIwQ"
    ],
    [
        "AgACAgIAAxkBAAITw2Hz0cCwnH-uuuzV0Z1iL6kqGXqAAALlvDEbTJmYS-f4GaWGPAHCAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAITxWHz0caK9M03wyprq80dGV-zvn8qAALmvDEbTJmYSzxfS_8NtMKyAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAITx2Hz0c4TPx-TtyJez8hNuRCLzvZJAALnvDEbTJmYSxiy9vl1WJYCAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAITyWHz0dZQSk4s7lPjsMj5CizbzNq0AALovDEbTJmYS-EnYp2q5uJ1AQADAgADbQADIwQ",
        "AgACAgIAAxkBAAITy2Hz0d3cmsCwmyjcrhWFzElxiq_cAALpvDEbTJmYS51VoDPRqxJDAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAITzWHz0eQaKv_Nz5jWncwc0_UO5vL4AALqvDEbTJmYS02ckS3ENrGcAQADAgADeQADIwQ",
        "AgACAgIAAxkBAAITz2Hz0fH9IwoQq0BFeWWXN_kD1b4vAALrvDEbTJmYS6jCnO7PTknMAQADAgADbQADIwQ",
        "AgACAgIAAxkBAAIT0WHz0gLWlGI6OA4OjpQfcGQE5LHVAALsvDEbTJmYS0_Fb8PrX8c4AQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIT02Hz0gnlE3-CScyMXjIBes82zHURAALtvDEbTJmYS1D2vtPuN-AZAQADAgADeAADIwQ",
        "AgACAgIAAxkBAAIT1WHz0hOkTZwo19Wa4q1Nyk-EFSVnAALuvDEbTJmYS8YxSNbuimLhAQADAgADeQADIwQ"
    ]
]

level_captions = [
    "Заробітчанин. Не жибрак, маю гроші",
    "Голова Сільради. Село то всьо моє",
    "Депутат міської ради. Я хачю вєласіпєд...",
    "Мер міста. Я раніше жив бідно, пас корови, продавав гриби. Одягався бідно. Мене ображали. Не вірили в "
    "мої таланти вчителі. Я не здався і доказав всім!",
    "Губернатор області. В Тернополі торчав катав у ширку дімідрол, я ненавидів поп я слухав тіко рок-н-рол",
    "Депутат Верховної Ради. КОЛИ ТЕБЕ НЕМААААА"
]

lvlup_requirements = [
    500,
    2000,
    8000,
    15000,
    30000
]

lvlup_rating = [
    3,
    10,
    20,
    50,
    120,
    300
]

money_earn_multiplier = [
    1, 3, 9, 27, 81, 243
]

work_text = [
    " жостко назбирав повний кошик трускавок пану!",
    " натиряв грошей з бюджету села!",
    " провів збір коштів на реконструкцію пам'ятника!",
    " відкрив нову школу в найзалупнішому районі міста!",
    " проклав дорогу до свого рідного села!",
    " зачитав текст, який йому дав олігарх, на трибуні ради!"
]

work_photos = [
    "AgACAgIAAxkBAAIErmHh1U3Y3aR2iLG17jGVB8_9XvloAAJmuDEb9xwQS-Ry7B8b6eR7AQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIEsGHh1bqKQfABCFf-i70s5xsq62MWAAJpuDEb9xwQS63g-PHzSoP6AQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIHjGHj-HLMK5u4ozcjaZ_krnFik-MxAAIZujEb2msgS30E1LSLhD0aAQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIPj2Hr-scC_2n2DkT4LKJGU5S1JmxLAAK4uDEbTFVhSxxdjS8sRAkAAQEAAwIAA3kAAyME",
    "AgACAgIAAxkBAAIQ82Huvw8sNS5Ht3Nr-EgrWT06oT4bAAO4MRu4AXlLnREmIFnwFG4BAAMCAAN5AAMjBA",
    "AgACAgIAAxkBAAIT12Hz01I_SUVk-Bed2i_vk_j7VSdLAAL0vDEbTJmYS6AeM8CrKcFBAQADAgADeQADIwQ"
]

not_working_photos = [
    "AgACAgIAAxkBAAIEsmHh2ByX9NgOCaRmkpETrJxLulgwAAJxuDEb9xwQS-5a-ouzRFdOAQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIEtGHh2No8CWpUkPZ4ZuwXOiu_SkcoAAJzuDEb9xwQS7zxAAHbX9q9SQEAAwIAA3gAAyME",
    "AgACAgIAAxkBAAIEtmHh2PHZ8T7jjiOjPI0vVDsd4FXrAAJ0uDEb9xwQS0HOefdMR3VFAQADAgADeQADIwQ",
    "AgACAgIAAxkBAAIEuGHh2UHSJaqZ4Ud4JC9GNMj98BoZAAJ2uDEb9xwQS70qbVku8wdlAQADAgADeQADIwQ",
    "AgACAgIAAxkBAAIEumHh2V3Op5aE6DVXXtK4PCIztZdmAAJ3uDEb9xwQS1yFqlB7qnXpAQADAgADeAADIwQ"
]

biz_name = [
    "👦🏼Сусідський піздюк",
    "👨🏿Негр",
    "🛒Кіоск"
]

biz_photos = [
    "AgACAgIAAxkBAAIIzGHkXpxYawqoig2yxtym27LL_o0TAALGuzEb9e4gS0qhKawtQfOfAQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIIzmHkXvZd8rhDV9dZUfllBVvvHf9xAALHuzEb9e4gS9xoHt_kegSzAQADAgADbQADIwQ",
    "AgACAgIAAxkBAAII0GHkXza4hRsHLqrMGljBEpCqJPOyAALIuzEb9e4gS7x0pvtNQO9RAQADAgADeQADIwQ"
]

biz_db_name = [
    "kid",
    "negr",
    "kiosk"
]

biz_prices = [
    100,
    500,
    3000
]

biz_provides = [
    50,
    100,
    400
]

biz_provide_text = [
    "Ви закупили малому пиваса і сигарет!",
    "Ви закупили негру хавчика!",
    "Ви закупили товар кіоску!"
]

biz_provide_photos = [
    "AgACAgIAAxkBAAIJ3WHmvKvJVxx6BhJGbHK0xz9aNJqaAAL8tDEbr-IxS0cXN1NNmaHKAQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIJ32HmvUFzRmYxvLt8zQ3XyxHFuWEdAAICtTEbr-IxS3A6py7E_Zq1AQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIJt2HmrPoymDaX5RPK_GzMrE_R24ywAAJytzEbkiQxS-B9cGTz2_eFAQADAgADeAADIwQ"
]


def biz_provide_buttons(result, i, price):
    if price:
        return str(result[i]) + ": " + biz_name[i] + ' ' + str(result[i] * biz_provides[i]) + '$'
    else:
        return str(result[i]) + ": " + biz_name[i]


biz_worked_text = [
    "Піздюк сьогодні вже збирав металолом!",
    "Негр вже відпрацював свою зміну!",
    "Кіоск вже приніс дохід за сьогодні!"
]

biz_work_text = [
    "Піздюк назбирав купу брухту і відніс на базу!💰 Дохід: $",
    "Негр передав гроші з Польщі!💰 Дохід: $",
    "Кіоск продав товар!💰 Дохід: $"
]

biz_not_visited_text = [
    "Піздюк не буде нічого робити без пиваса і сіг!",
    "Негр зголоднів у йобаній Польщі, бо ти не погодував його!",
    "Кіоск вже розпродав весь товар!"
]

biz_rating_drop = [
    1, 3, 12
]

biz_rating_text = [
    f"Бомж побачив піздюка на пункті прийому металу і розпиздів про вас всьому селу!"
    f" Ваш рейтинг у громади впав на {biz_rating_drop[0]} пункт.",
    f"Сусідка побачила як ви відмиваєте негра у ванній! Рейтинг серед громади впав на {biz_rating_drop[1]} пункти",
    f"Отець Михайло побачив як ви відбудовуєте кіоск, тим самим створюючи конкуренцію кіоску його брата! На ранковій "
    f"молитві він вирішив розказати всім, що ви трахали козу! Рейтинг серед громади впав на {biz_rating_drop[2]} "
    f"пунктів "
]

biz_rating_photo = [
    "AgACAgIAAxkBAAILXmHn-7kdnfJX5gmUOCqD_rhE0Br0AAIUtTEbr-JBS0JWDIsILqcuAQADAgADbQADIwQ",
    "AgACAgIAAxkBAAILYGHn_BdkZ9afLED45r5R-mnBl7DuAAIVtTEbr-JBS8jVfwg5AudaAQADAgADeQADIwQ",
    "AgACAgIAAxkBAAILYmHn_GqA56UFPOlgHinktLZ7LHgrAAIXtTEbr-JBS_PiJab0OTCWAQADAgADeAADIwQ"
]

biz_profits = [
    5, 28, 140
]

biz_help = "👦🏼Сусідський піздюк:\nВ депутата за парканом живе мікрочел 8 років, який хоче купляти собі пиво і " \
           "дзигари, але він байстрюк і ніхто не вірить, шо він купує це діло \"для баті\". Купивши піздюка, " \
           "ви змушені купляти йому пивас кожного тижня, натомість він буде здавати всяке гавно на металолом, " \
           "а виручені гроші приносити вам кожного дня.\n\n👨🏿Негр:\nТвій кум возить до міста машини з Америки, " \
           "а в одній з них виявився негр. Тепер ця мавпочка живе в сараї кума. Викупивши в кума негра, " \
           "тобі необхідно купувати йому продовольчих продуктів кожен тиждень, він у свою чергу буде ганяти в Польщу " \
           "на трускавки і передавати гроші кожен день.\n\n🛒Кіоск:\nПісля того як бабка Зоя вмерла, її внукам у " \
           "спадок припав кіоск в селі. Внуки виставили кіоск на продаж, оскільки живуть в місті і той сраний кіоск " \
           "їм нахуй не всрався. Купивши кіоск треба кожного тижня закупляти товар, натомість кожного дня кіоск буде " \
           "приносити прибуток, фіксована частина якого буде відходити продавцеві як зарплата. "


biz_text = "Доступні види бізнесу:\n"

rating_up = [
    1, 2, 8
]

rating_price = [
    50, 80, 250
]

rating_name = [
    "Ящик горілки куму",
    "Дві свині для баби Каті",
    "Велопарковка біля ратуші"
]

sad_sticker = "CAACAgIAAxkBAAIF0mHi2qUiAib-CGg03DeTgHw-2B9KAAKdAAOzvVMzmb7zau0EAzIjBA"
happy_sticker = "CAACAgIAAxkBAAIF1GHi2z8pUJU9JNPh9mYXJfaK4lC7AAK1AAP-HBsMzkiZEJFJad0jBA"
what_sticker = "CAACAgIAAxkBAAIGfmHjCQ3ODK4nKZmnER5lv7wf-Q6hAAJuAAP3zNQYXCr47a4zAAGDIwQ"
money_pagulich_sticker = "CAACAgIAAxkBAAIIj2HkTmFJ-1E6aO_d2bjXXqFgzof-AAIpAAMwbFkgc0I6fExuM0QjBA"
money_valakas_sticker = "CAACAgIAAxkBAAIIk2HkTsGHDte6YbztwUAyV7lFRL4jAAKoAAMZ8nUb9i7wzt6UMxcjBA"

help_text = "Команди бота для використання в усіх чатах:\n/get - отримати свого депутата\n/show - оглянути основні " \
            "характеристики депутата\n/work - відправити депутата на заробітки (доступно 1 раз в день, точний час " \
            "бота за командою /time)\n/show_business - оглянути бізнес(и) депутата\n/lvlup - підвищити рівень " \
            "депутата (підвищує дохід від /work)\n/kill - вбити депутата\n/killed - кількість власних, " \
            "вбитих депутатів\n/time - отримати час бота\n\nКоманди бота для використання у розмові з " \
            "ботом:\n/business - зібрати дохід з бізнесу (1 раз на день)\n/provide_business - забезпечити бізнес " \
            "ресурсами (1 раз на тиждень, збивається для всіх бізнесів даної категорії при купівлі нового бізнесу " \
            "цієї ж категорії)\n/buy_business - купити бізнес (шанс бути поміченим 20%)\n/rating - підняти рейтинг " \
            "депутату"
