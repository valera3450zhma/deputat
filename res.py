MAX_LEVEL = 3

SU = [
    506126580,
    507028811
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
    ]
]

level_captions = [
    "Заробітчанин. Не жибрак, маю гроші",
    "Голова Сільради. Село то всьо моє",
    "Депутат міської ради. Не гордому мужику не горде місто"
]

lvlup_requirements = [
    500,
    2000,
    10000
]

money_earn_multiplier = [
    1, 3, 9, 27, 81, 243
]

work_text = [
    " жостко назбирав повний кошик трускавок пану!",
    " натиряв грошей з бюджету села!",
    " провів збір коштів на реконструкцію пам'ятника!"
]

work_photos = [
    "AgACAgIAAxkBAAIErmHh1U3Y3aR2iLG17jGVB8_9XvloAAJmuDEb9xwQS-Ry7B8b6eR7AQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIEsGHh1bqKQfABCFf-i70s5xsq62MWAAJpuDEb9xwQS63g-PHzSoP6AQADAgADeAADIwQ",
    "AgACAgIAAxkBAAIHjGHj-HLMK5u4ozcjaZ_krnFik-MxAAIZujEb2msgS30E1LSLhD0aAQADAgADeAADIwQ"
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

biz_help = "Сусідський піздюк:\nВ депутата за парканом живе мікрочел 8 років, який хоче купляти собі пиво і дзигари, " \
           "але він байстрюк і ніхто не вірить, шо він купує це діло \"для баті\". Купивши піздюка, ви змушені " \
           "купляти йому пивас кожного тижня, натомість він буде здавати всяке гавно на металолом, а виручені гроші " \
           "приносити вам кожного дня.\n\nНегр:\nТвій кум возить до міста машини з Америки, а в одній з них виявився " \
           "негр. Тепер ця мавпочка живе в сараї кума. Викупивши в кума негра, тобі необхідно купувати йому " \
           "продовольчих продуктів кожен тиждень, він у свою чергу буде ганяти в Польщу на трускавки і передавати " \
           "гроші кожен день.\n\nКіоск:\nПісля того як бабка Зоя вмерла, її внукам у спадок припав кіоск в селі. " \
           "Внуки виставили кіоск на продаж, оскільки живуть в місті і той сраний кіоск їм нахуй не всрався. Купивши " \
           "кіоск треба кожного тижня закупляти товар, натомість кожного дня кіоск буде приносити прибуток, " \
           "фіксована частина якого буде відходити продавцеві як зарплата."


biz_text = "Доступні види бізнесу:\n"


sad_sticker = "CAACAgIAAxkBAAIF0mHi2qUiAib-CGg03DeTgHw-2B9KAAKdAAOzvVMzmb7zau0EAzIjBA"
happy_sticker = "CAACAgIAAxkBAAIF1GHi2z8pUJU9JNPh9mYXJfaK4lC7AAK1AAP-HBsMzkiZEJFJad0jBA"
what_sticker = "CAACAgIAAxkBAAIGfmHjCQ3ODK4nKZmnER5lv7wf-Q6hAAJuAAP3zNQYXCr47a4zAAGDIwQ"
money_pagulich_sticker = "CAACAgIAAxkBAAIIj2HkTmFJ-1E6aO_d2bjXXqFgzof-AAIpAAMwbFkgc0I6fExuM0QjBA"
money_valakas_sticker = "CAACAgIAAxkBAAIIk2HkTsGHDte6YbztwUAyV7lFRL4jAAKoAAMZ8nUb9i7wzt6UMxcjBA"
