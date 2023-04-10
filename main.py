import config
import logging
import openai
import asyncio
from aiogram import Bot, Dispatcher, executor, types

# log
logging.basicConfig(level=logging.INFO)

# init openai
openai.api_key = config.OPENAI_TOKEN

# init aiogram
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def gpt_answer(message: types.Message):
    # await message.answer(message.text)

    model_engine = "text-davinci-003"
    max_tokens = 128  # default 1024
    prompt = message.text
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    await message.answer("ChatGPT: Генерую відповідь ...")
    await message.answer(completion.choices[0].text)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

