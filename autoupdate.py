import os
import sys
import random
import signal
from time import sleep
from os.path import join, dirname
from threading import Thread
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def signal_handler():
    print('You pressed Ctrl+C')
    sys.exit(0)


class AutoUpdater(Thread):
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) ' \
                 'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                 'Version/13.0.3 Mobile/15E148 Safari/604.1'

    selenium_options = ('--disable-notifications',
                        '--log-level=1',
                        # '--headless',
                        '--window-size=480,800',
                        f'--user-agent={user_agent}')

    def __init__(self, login, pwd, *args, **kwargs):
        super().__init__()
        self.login = login
        self.pwd = pwd
        self.refresh_count = 0
        self.timeout = 3
        self.options = webdriver.ChromeOptions()
        for option in selenium_options:
            self.options.add_argument(option)
        self.driver = webdriver.Chrome(options=self.options)
        self.daemon = True
        self.start()

    def _find_element(self, xpath_selector):
        try:
            element_present = EC.element_located_to_be_selected((By.XPATH, xpath_selector))
            WebDriverWait(self.driver, self.timeout).until(element_present)
        except TimeoutException:
            pass
        try:
            return self.driver.find_element_by_xpath(xpath_selector)
        except NoSuchElementException:
            return None

    def run(self):
        self.driver.get(self.start_url)

        # ищем необходимые input формы
        user_input = self._find_element(self.xpath_user_input)
        pwd_input = self._find_element(self.xpath_pwd_input)

        # вводим логин и пароль
        user_input.send_keys(self.login)
        pwd_input.send_keys(self.pwd)
        pwd_input.send_keys(Keys.RETURN)

        while True:
            # ищем активные кнопки обновления резюме
            update_btns = self._find_element(self.xpath_update_btns)

            # если кнопки есть, прокликиваем с задержкой
            if update_btns:
                print(f'[{self.__class__.__name__}][{self.login}]\t - found {len(update_btns)} active buttons')

                for update_btn in update_btns:
                    cv_name = update_btn.find_element_by_xpath(self.xpath_update_btn).text
                    print(f'[{self.__class__.__name__}][{self.login}]\tupdating {cv_name}...')
                    update_btn.click()
                    sleep(1)

            # sleep(random.randint(250, 400))
            sleep(random.randint(1, 4))
            print(f'[{self.__class__.__name__}][{self.login}]\t[{self.refresh_count}]\treloading page...')
            self.driver.refresh()
            self.refresh_count += 1


class HhruAutoUpdate(AutoUpdater):
    def __init__(self, login, pwd, *args, **kwargs):
        self.start_url = 'https://m.hh.ru/applicant/resumes'
        self.xpath_user_input = '//input[@name="username"]'
        self.xpath_pwd_input = '//input[@name="password"]'
        self.xpath_update_btns = '//button[@data-qa="resumes-update"]'
        self.xpath_update_btn = '../../form/../../a//h3'
        super().__init__(login, pwd, *args, **kwargs)


class SuperJobAutoUpdate(AutoUpdater):
    def __init__(self, login, pwd, *args, **kwargs):
        self.start_url = 'https://www.superjob.ru/user/resume/'
        self.xpath_user_input = '//input[contains(@class, "f-test-input-login")]'
        self.xpath_pwd_input = '//input[contains(@class, "f-test-input-password")]'
        self.xpath_update_btns = '//button[contains(@class, "f-test-button-Obnovit_datu")]'
        self.xpath_update_btn = '../../../../../div/div[1]/div[2]/a/div/div[1]/div[1]'
        super().__init__(login, pwd, *args, **kwargs)


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) ' \
                 'AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                 'Version/13.0.3 Mobile/15E148 Safari/604.1'
    selenium_options = ('--disable-notifications',
                        '--log-level=1',
                        '--window-size=480,800',
                        f'--user-agent={user_agent}')

    # //TODO переделать хранение паролей, в окружении небезопасно
    do_env = join(dirname(__file__), '.env')
    load_dotenv(do_env)

    OLEG_LOGIN = os.getenv('OLEG_LOGIN')
    OLEG_HHRU_PWD = os.getenv('OLEG_HHRU_PWD')
    OLEG_SUPERJOB_PWD = os.getenv('OLEG_SUPERJOB_PWD')

    JULIA_LOGIN = os.getenv('JULIA_LOGIN')
    JULIA_HHRU_PWD = os.getenv('JULIA_HHRU_PWD')

    # HhruAutoUpdate(JULIA_LOGIN, JULIA_HHRU_PWD)
    # HhruAutoUpdate(OLEG_LOGIN, OLEG_HHRU_PWD)
    SuperJobAutoUpdate(OLEG_LOGIN, OLEG_SUPERJOB_PWD)

    signal.signal(signal.SIGINT, signal_handler)
    while True:
        _input = input('Press Ctrl+C to exit\n')
