import pytest
import requests
import allure

from helpers.helpers import Person
from data.urls import URL, Endpoints
from data.status_code import StatusCode


@pytest.fixture
def create_new_user():
    with allure.step("Создать тестового пользователя"):
        payload = Person.create_data_correct_user()
        with allure.step("Отправить POST запрос для создания пользователя"):
            response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=payload)

    # Передаём данные в тест
    yield payload, response

    # Пост-условие: удалить тестового пользователя
    with allure.step("Удалить тестового пользователя"):
        if response.status_code == StatusCode.OK and response.json().get("success"):
            token = response.json()["accessToken"]
            with allure.step("Отправить DELETE запрос для удаления пользователя"):
                requests.delete(
                    URL.main_url + Endpoints.DELETE_USER,
                    headers={"Authorization": token},
                )
