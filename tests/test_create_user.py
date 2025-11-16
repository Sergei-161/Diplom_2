import pytest
import allure
import requests

from helpers.helpers import Person
from data.urls import URL, Endpoints
from data.status_code import StatusCode
from data.text_response import TextResponse


class TestCreateUser:

    @allure.title('Проверка создания уникального пользователя')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Проверяем ответ.
                        ''')
    def test_create_unique_user_is_created(self, create_new_user):
        payload, response = create_new_user

        with allure.step("Проверить ответ создания пользователя"):
            assert response.status_code == StatusCode.OK
            assert response.json().get("success") is True

    @allure.title('Проверка создания пользователя, который уже зарегистрирован')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Получаем данные для регистрации;
                        3. Отправляем повторный запрос на создание пользователя;
                        4. Проверяем ответ.
                        ''')
    def test_create_double_user_is_not_created(self, create_new_user):
        payload, create_response = create_new_user

        with allure.step("Отправить повторный POST запрос для создания пользователя"):
            response_double_register = requests.post(
                URL.main_url + Endpoints.CREATE_USER,
                data=payload,
            )

        with allure.step("Проверить ответ повторного создания пользователя"):
            assert response_double_register.status_code == StatusCode.FORBIDDEN
            assert (
                response_double_register.json().get("message")
                == TextResponse.CREATE_DOUBLE_USER
            )

    @allure.title('Проверка создания пользователя без одного обязательного поля')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя без одного поля;
                        2. Проверяем ответ.
                        ''')
    @pytest.mark.parametrize('payload', [
        Person.create_user_without_email(),
        Person.create_user_without_name(),
        Person.create_user_without_password(),
    ])
    def test_create_user_no_required_fields_is_not_created(self, payload):
        with allure.step("Отправить POST запрос для создания пользователя без обязательного поля"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_USER,
                data=payload,
            )

        with allure.step("Проверить ответ создания пользователя без обязательного поля"):
            assert response.status_code == StatusCode.FORBIDDEN
            assert response.json().get("success") is False
