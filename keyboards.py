from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import emoji
btn_start = KeyboardButton(f'{emoji.PLAY_BUTTON} старт')
btn_time = KeyboardButton(f'{emoji.TIMER_CLOCK} время')
btn_info = KeyboardButton(f'{emoji.INFORMATION} инфо')
btn_games = KeyboardButton(f'{emoji.PLAY_BUTTON} игры')
btn_return = KeyboardButton(f'{emoji.BACK_ARROW} вернуться')
btn_rock = KeyboardButton(f'{emoji.ROCK} Камень')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} Хожницы')
btn_paper = KeyboardButton(f'{emoji.NOTEBOOK} Бумага')
btn_value = KeyboardButton(f'{emoji.COIN} Койны')
btn_quest = KeyboardButton(f'{emoji.WORLD_MAP} Квест')
btn_rock_scissors_paper = KeyboardButton(f'{emoji.VIDEO_GAME} Камень,Ножниц,Бумага')
btn_image = KeyboardButton(f'{emoji.CITYSCAPE} изображения')
btn_numbers = KeyboardButton(f'{emoji.INPUT_NUMBERS} угадай число')

inline_kb_choice_side = InlineKeyboardMarkup([
    [InlineKeyboardButton('пойти налево',callback_data='left_side')],
    [InlineKeyboardButton('пойти направо', callback_data='right_side')]
])

inline_kb_left_side = InlineKeyboardMarkup([
    [InlineKeyboardButton('побежать на волка',callback_data='run_forward')],
    [InlineKeyboardButton('убежать от волка', callback_data='run')],
    [InlineKeyboardButton('взять палку и напасть',callback_data='stick')]
])

inline_kb_right_side = InlineKeyboardMarkup([
    [InlineKeyboardButton('идти дальше',callback_data='city')],
    [InlineKeyboardButton('вернутся',callback_data='back')]
])

InlineKeyboardButton('Пройти квест',
                     callback_data='start_quest')

inline_kb_start_quest = InlineKeyboardMarkup([
[InlineKeyboardButton('Пройти квест',
                    callback_data='start_quest')]
    ])
kb_games = ReplyKeyboardMarkup(
    keyboard=[
        [btn_quest,btn_rock_scissors_paper,btn_numbers,
        btn_return]
    ],
    resize_keyboard = True
)
kb_main = ReplyKeyboardMarkup(
    keyboard=[
        [btn_start, btn_time, btn_info, btn_games, btn_image],
         [btn_return, btn_value]
    ],
    resize_keyboard = True
)
kb_rps = ReplyKeyboardMarkup(
    keyboard=[
        [btn_rock, btn_scissors, btn_paper],
        [btn_return, ]
    ],
    resize_keyboard=True
)