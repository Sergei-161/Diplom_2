import allure
import requests

from helpers.helpers import Person
from data.urls import URL, Endpoints
from data.status_code import StatusCode


class TestLoginUser:

    @allure.title('Проверка логин под существующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на логин в системе;
                        3. Проверяем ответ.
                        ''')
    def test_login_user(self, create_new_user):
        payload, _ = create_new_user

        with allure.step("Отправить POST запрос для логина пользователя"):
            login = requests.post(
                URL.main_url + Endpoints.LOGIN,
                data=payload,
            )

        with allure.step("Проверить ответ логина пользователя"):
            assert login.status_code == StatusCode.OK
            assert login.json().get("success") is True

    @allure.title('Проверка логин под несуществующим пользователем')
    @allure.description('''
                        1. Отправляем запрос на логин в системе без регистрации;
                        2. Проверяем ответ.
                        ''')
    def test_login_under_none_user(self):
        with allure.step("Отправить POST запрос для логина несуществующего пользователя"):
            login = requests.post(
                URL.main_url + Endpoints.LOGIN,
                data=Person.create_user_without_name(),
            )

        with allure.step("Проверить ответ логина несуществующего пользователя"):
            assert login.status_code == StatusCode.UNAUTHORIZED
            assert login.json().get("success") is False
