""" Авторизация на wildberries. Каптчу и СМС код нужно брать из ТГ-бота
"""
import pickle
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from config import login
from loader import dp
from services import delay, get_web_driver_options
from state import CaptchaAndPhoneState
from parser_wildberris import wb_parser
from logger import logger


driver = get_web_driver_options()


def auth_to_wb():
    """ Логиниться на wildberries
    """
    try:
        driver.get("https://www.wildberries.ru/security/login")
        driver.find_element(By.CLASS_NAME, 'input-item').send_keys(login)
        delay()
        driver.find_element(By.ID, 'requestCode').click()
        delay()
        img = driver.find_element(By.CLASS_NAME, 'captcha-image')
        delay()
        src = img.get_attribute('src')
        urlretrieve(src, "captcha_img/captcha.png")
        delay()
    except Exception as e:
        print(e)


@logger.catch
@dp.message_handler(state=CaptchaAndPhoneState.captcha)
async def set_captcha(message: Message):
    if driver.find_element(By.ID, 'smsCaptchaCode'):
        captcha = message.text
        driver.find_element(By.ID, 'smsCaptchaCode').send_keys(captcha)
        delay()
        driver.find_element(By.CLASS_NAME, 'c-btn-main-lg-v1').click()
        delay()
    await message.answer('Введите код из СМС !')
    await CaptchaAndPhoneState.phone.set()


@logger.catch
@dp.message_handler(state=CaptchaAndPhoneState.phone)
async def get_sms_code_phone(message: Message, state: FSMContext):
    try:
        sms_code_phone = message.text
        driver.find_element(By.CLASS_NAME, 'j-input-confirm-code').send_keys(
            sms_code_phone)
        delay()
        pickle.dump(driver.get_cookies(), open(f"cookies/{login}_cookies", "wb"))
        # driver.find_element(By.ID, 'requestCode').click()
        delay()
        await message.answer('Вы успешно авторизовались!')
        await state.finish()
        wb_parser()
    except Exception as e:
        logger.warning(e)
    finally:
        driver.close()
        driver.quit()




