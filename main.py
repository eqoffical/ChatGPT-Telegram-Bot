import config
import logging
import openai
import asyncio
import time
from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# launch time
start_time = time.time()

# init openai
openai.api_key = config.OPENAI_TOKEN

# init aiogram
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# /help command
@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer("Доступні команди:\n"
                         "/help - Показує всі доступні команди\n"
                         "/chat - Поговорити з ботом / задати питання\n"
                         "/status - Показати поточний стан боту")

# /start command
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привіт 👋\n"
                        "Чим я можу вам допомогти?\n"
                        "Напишіть /help щоб побачити всі доступні команди.")

# /chat command
@dp.message_handler(commands=['chat'])
async def cmd_chat(message: types.Message):
    # remove the '/chat' command from the user's message to get the question
    question = message.text.replace('/chat', '', 1).strip()
    if question:
        model_engine = "text-davinci-003"
        max_tokens = 1024  # default 1024
        prompt = question
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        await message.answer("Думаю . . .")
        await message.answer(completion.choices[0].text)
    else:
        await message.answer("Будь ласка, напишіть /chat разом зі своїм запитанням.\n"
                            "Наприклад: /chat коли був створений python?")


# /status command
@dp.message_handler(commands=['status'])
async def cmd_status(message: types.Message):
    current_time = time.time() # current time
    elapsed_time = int(current_time - start_time) # time elapsed since the bot was launched in seconds
    hours, rem = divmod(elapsed_time, 3600) # converting time to hours, minutes, and seconds
    minutes, seconds = divmod(rem, 60)
    
    status_message = f"Я онлайн і готовий до спілкування!\n"
    status_message += f"Я тут сижу вже: {hours:02d}:{minutes:02d}:{seconds:02d}"
    await message.answer(status_message)

# message handler
@dp.message_handler(commands=['help', 'chat', 'status'])
async def gpt_answer(message: types.Message):
    pass

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
