from pyrogram import Client, filters
from pyrogram.types import ForceReply
from FusionBrain_AI import generate

import config
import datetime
import keyboards
import random
import json
import base64


user_games = {}

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name='my bot'
)



def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command('info') | button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply('/info'
                        '/time'
                        '/start')

@bot.on_message(filters.command('time') | button_filter(keyboards.btn_time))
async def time(bot, message):
    await message.reply(f'время:{datetime.datetime.now()}')

@bot.on_message(filters.command('start') | button_filter(keyboards.btn_start))
async def start(bot, message):
    await message.reply('добро пожаловать')
    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEO2-NoaP90Jcpl4Wo5fEChT82NTNI29wACEgADwDZPEzO8ngEulQc3NgQ',
    reply_markup=keyboards.kb_main)
    with open('users.json', 'r') as file:
        users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open('users.json', 'w') as file:
            json.dump(users, file)

@bot.on_message(filters.command('games') | button_filter(keyboards.btn_rock_scissors_paper))
async def game(bot, message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >= 10:
        await message.reply('Твой ход', reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f'Не хватает средств,На твоём счету{users[str(message.from_user.id)]}, минимальная сумма для игры - 10')

@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_scissors) |
                button_filter(keyboards.btn_paper))
async def choice_rps(bot, message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    rock = keyboards.btn_rock.text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text
    user = message.text
    ai = random.choice([rock, scissors, paper])
    if user == ai:
        await message.reply('ничья')
    elif (user == rock and ai == scissors) or\
        (user == scissors and ai == paper) or\
        (user == paper and ai == rock):
        await message.reply(f'ты выйграл.Бот выбрал {ai}, ты заработал 10 койнов',
                            reply_markup=keyboards.kb_rps)
        users[str(message.from_user.id)] += 10
    else:
        await message.reply(f'ты пройграл. Бот выбрал {ai}, ты потерял 10 койнов',
                            reply_markup=keyboards.kb_rps)
        users[str(message.from_user.id)] -= 10
    with open('users.json', 'w') as file:
        json.dump(users, file)

@bot.on_message(filters.command('return')| button_filter (keyboards.btn_return))
async def back(bot, message):
    await message.reply('возврат в главное меню', reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('value')| button_filter (keyboards.btn_value))
async def value(bot, message):
    with open('users.json', 'r') as file:
        users = json.load(file)
    await message.reply(f'твой койны:{users[str(message.from_user.id)]}')

@bot.on_message(filters.command('game1')| button_filter (keyboards.btn_games))
async def games(bot, message):
    await message.reply(f'вот игры:',
        reply_markup=keyboards.kb_games)

@bot.on_message(filters.command('quest') | button_filter(keyboards.btn_quest))
async def kvest(bot, message):
    await message.reply_text('Хотите ли вы отправиться в путешествие,полное приключений и загадок?', reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == 'start_quest':
        await bot.answer_callback_query(query.id,
            text='Добро пожаловать в квест под названием Вернись С Леса',
            show_alert=True)
        await query.message.reply_text('ты проснулся посреди леса.Куда пойдёшь?',
                                reply_markup=keyboards.inline_kb_choice_side)
    elif query.data == 'left_side':
        await query.message.reply_text('Ты пошёл налево,ты шёл примерно 5 минут,'
                                       'ты увидел волка,что ты будешь делать?:',
                                reply_markup=keyboards.inline_kb_left_side)
    elif query.data == 'right_side':
        await query.message.reply_text('Ты пошёл налево,ты шёл примерно 5 минут,ты увидел свет,пойти дальше?',
                                       reply_markup=keyboards.inline_kb_right_side)
    elif query.data == 'run_forward':
        await query.message.reply_text('Ты побежал на волка,он зарычал,ты испугался и убхежал,ты вернулся в начало',
                                       reply_markup=keyboards.inline_kb_choice_side)
    elif query.data == 'run':
        await query.message.reply_text('Ты убежал на волка и вернулся в начало',
                                       reply_markup=keyboards.inline_kb_choice_side)
    elif query.data == 'stick':
        await query.message.reply_text('Ты взял палку и побежал на волка,он испугался и убежал,ты увидел город и вернулся домой!'
                                       'У тебя получилось вернутся,молодец!',
                                       reply_markup=keyboards.kb_main)
    elif query.data == 'back':
        await query.message.reply_text('Ты верулся',
                                       reply_markup=keyboards.inline_kb_choice_side)
    elif query.data == 'city':
        await query.message.reply_text('Ты пошёл в свет и ты увидел город!'
                                       'Тебе повезло ты вернулся домой!')
    await query.message.delete()

@bot.on_message(filters.command('image'))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/image', '')
        await message.reply_text(f'Генерирую изображение по запросу ({query}), подождите немного...')
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f'images/image.jpg', 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg',
                                                reply_to_message_id=message.id)
        else:
            await message.reply_text('возникла ошибка,попробуйте ещё раз',
                                     raply_to_message_id=message.id)
    else:
        await message.reply_text('Введите запрос')

query_text = ('введи запрос для генераций например:image<твой запрос>')
@bot.on_message(button_filter(keyboards.btn_image))
async def image_command(bot, message):
    await message.reply('введи запрос для генераций например:image<твой запрос>',
                        query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f'Генерирую изображение по запросу **{query}**.Ожидание около минуты')
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f'images/image.jpg', 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg',
                                 reply_to_message_id=message.id)
        else:
           await message.reply_text('возникла ошибка,попробуйте ещё раз',
                                     raply_to_message_id=message.id)
    else:
        await message.reply_text('Возникала ошибка, попробуйте ещё раз',
                                 reply_to_message_id=message.id,
                                 reply_markup=keyboards.kb_main)

@bot.on_message(button_filter(keyboards.btn_numbers))
async def numbers(bot, message):
    random_num = random.randint(1, 100)
    message = await message.reply_text('Если ты готов,то напиши первое число')
    user_id = message.from_user.id
    user_games[user_id] = {'number': random_num,
                      'message_id': message.id,
                      'attempts': 10}

@bot.on_message()
async def guess_number(bot, message):
    global user_games
    user_id = message.from_user.id
    if user_id not in user_games:
        random_num = random.randint(1, 100)
        user_games[user_id] = {
            'number': random_num,
            'attempts': 9
        }
        await message.reply('перед тем как сказать подсказку,я предупреждаю то-что число не больше 100')
    guess = int(message.text)
    game = user_games[user_id]
    if game['attempts'] == 0:
        await message.reply(f'у тебя закончились попытки,я загадал число {game['number']} удачи в следующий раз:)',
                            reply_markup=keyboards.kb_main)
        del game[user_id]
    elif guess < game['number']:
        await message.reply(f'ты не угадал,число больше,у тебя осталось {game['attempts']} попыток')
        game['attempts'] -= 1
    elif guess > game['number']:
        await message.reply(f'ты не угадал,число меньше,у тебя осталось {game['attempts']} попыток')
        game['attempts'] -= 1
    elif guess == game['number']:
        await message.reply('ты угадал число!',
                            reply_markup=keyboards.kb_main)
        del user_games[user_id]
    else:
        await message.reply('извини,но ты наверное вообще не цифру написал')

bot.run()
