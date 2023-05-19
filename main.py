import config
import logging
import openai
import asyncio
import time
from aiogram import Bot, Dispatcher, executor, types

username = '' # PUT HERE YOUR USERNAME
logging.basicConfig(level=logging.INFO) # log
start_time = time.time() # launch time
count_requests = 0 # counting variable
openai.api_key = config.OPENAI_TOKEN # init openai
bot = Bot(token=config.TOKEN) # init aiogram
dp = Dispatcher(bot)

# /help command
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Доступні команди:\n"
                         "/help - Показує всі доступні команди\n"
                         "/chat - Поговорити зі мною / задати питання\n"
                         "/status - Показати поточний стан боту\n"
                         "/git - Мій репозиторій GitHub\n"
                         "/kill - Може не треба?")

# /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привіт 👋\n"
                        "Чим я можу вам допомогти?\n"
                        "Напишіть /help щоб побачити всі доступні команди")

# /chat command
@dp.message_handler(commands=['chat'])
async def cmd_chat(message: types.Message):
    global count_requests

    bot_username = (await bot.get_me()).username # Get the bot's username

    # Check if the bot name is mentioned in the message
    if f'@{bot_username}' in message.text:
        prompt = message.text.replace(f'/chat@{bot_username}', '', 1).strip() # Extract the prompt by removing the '/chat@botname' part
    else:
        prompt = message.text.replace('/chat', '', 1).strip() # Remove the '/chat' command from the user's message to get the question

    if prompt:
        await message.answer("Думаю . . .")
        model_engine = "gpt-3.5-turbo"
        max_tokens = 1024  # default 1024
        completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "Ви - користувач"},
                {"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.6,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        if completion.choices:
            bot_reply = completion.choices[0].message['content']
            await message.reply(bot_reply)
            count_requests += 1  # counting
        else:
            await message.reply("Вибачте, я не придумав 😔\n"
                                "Напишіть, будь ласка, ще раз")

    else:
        await message.reply("Будь ласка, напишіть /chat разом зі своїм запитанням.\n"
                            "Наприклад: /chat коли був створений python?")

# /status command
@dp.message_handler(commands=['status'])
async def cmd_status(message: types.Message):
    current_time = time.time() # current time
    elapsed_time = int(current_time - start_time) # time elapsed since the bot was launched in seconds
    hours, rem = divmod(elapsed_time, 3600) # converting time to hours, minutes, and seconds
    minutes, seconds = divmod(rem, 60)

    # ukrainian counting system 
    count = count_requests
    if count % 10 == 1 and count % 100 != 11:
        times = "раз"
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        times = "рази"
    else:
        times = "разів"
    
    # add the chat command count to the status message
    status_message = f"Я онлайн і готовий до спілкування!\n"
    status_message += f"Я тут сижу вже: {hours:02d}:{minutes:02d}:{seconds:02d}\n"
    status_message += f"Сьогодні зі мною спілкувалися {count} {times} 👀"
    
    await message.answer(status_message)


# /git command
@dp.message_handler(commands=['git'])
async def cmd_help(message: types.Message):
    link = "https://github.com/eqoffical/ChatGPT-Telegram-Bot.git"
    await message.answer("Ось посилання на мій репозиторій <a href='{}'>GitHub</a>".format(link), parse_mode=types.ParseMode.HTML)

# /kill command
@dp.message_handler(commands=['kill'])
async def cmd_kill(message: types.Message):
    if message.from_user.username == username: 
        await message.reply("Я пішов спати 😴\n"
                            "На добраніч!")
        # Stop the event loop
        await dp.storage.close()
        await dp.storage.wait_closed()
        exit()
    else:
        await message.reply("Ви хочете мене вбити?!😨\n"
                            "Вбивця!")

# message handler
@dp.message_handler(commands=['help', 'chat', 'status', 'git', 'kill'])
async def gpt_answer(message: types.Message):
    pass

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
