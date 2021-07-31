#!/usr/bin/python3
""" Исполняемый файл
"""
import logging
import os

from aiogram.types import Message
from aiogram.utils import executor

from config import login
from loader import dp, bot
from logger import logger
from login_to_wb import auth_to_wb
from state import CaptchaAndPhoneState
from parser_wildberris import wb_parser


@logger.catch
@dp.message_handler(commands='start')
async def start(message: Message):
    if not os.path.exists('captcha_img'):
        os.mkdir('captcha_img')

    auth_to_wb()

    await bot.send_photo(
        message.chat.id,
        photo=open('captcha_img/captcha.png', 'rb')
    )
    await message.answer('Введите каптчу:')
    await CaptchaAndPhoneState.captcha.set()


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook()


if __name__ == '__main__':
    if os.path.exists(f'cookies/{login}_cookies'):
        wb_parser()
    else:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)

