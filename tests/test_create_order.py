import requests
import allure

from helpers.helpers import Ingredients
from data.urls import URL, Endpoints
from data.status_code import StatusCode
from data.text_response import TextResponse


class TestCreateOrder:

    @allure.title('Проверка создания заказа авторизованным пользователем')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа с авторизацией;
                        3. Проверяем ответ.
                        ''')
    def test_create_order_whith_auth_is_created(self, create_new_user):
        _, create_response = create_new_user
        token = create_response.json()["accessToken"]
        headers = {'Authorization': token}

        with allure.step("Отправить POST запрос для создания заказа с авторизацией"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_ORDER,
                headers=headers,
                data=Ingredients.correct_ingredients_data,
            )

        with allure.step("Проверить ответ создания заказа с авторизацией"):
            assert response.status_code == StatusCode.OK
            assert response.json().get("success") is True

    @allure.title('Проверка создания заказа без авторизации')
    @allure.description('''
                        1. Отправляем запрос на создание заказа без авторизации;
                        2. Проверяем ответ.
                        ''')
    def test_create_order_without_auth_is_created(self):
        with allure.step("Отправить POST запрос для создания заказа без авторизации"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_ORDER,
                data=Ingredients.correct_ingredients_data,
            )

        with allure.step("Проверить ответ создания заказа без авторизации"):
            assert response.status_code == StatusCode.OK
            assert response.json().get("success") is True

    @allure.title('Проверка создания заказа авторизованным пользователем c ингредиентами')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа с передачей ID ингредиентов с авторизацией;
                        3. Проверяем ответ.
                        ''')
    def test_create_order_whith_ingredients_is_created(self, create_new_user):
        _, create_response = create_new_user
        token = create_response.json()["accessToken"]
        headers = {'Authorization': token}

        with allure.step("Отправить POST запрос для создания заказа с ингредиентами"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_ORDER,
                headers=headers,
                data=Ingredients.correct_ingredients_data,
            )

        with allure.step("Проверить ответ создания заказа с ингредиентами"):
            assert response.status_code == StatusCode.OK
            assert response.json().get("success") is True

    @allure.title('Проверка создания заказа авторизованным пользователем без ингредиентов')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа без ингредиентов с авторизацией;
                        3. Проверяем ответ.
                        ''')
    def test_create_order_whithout_ingredients_is_not_created(self, create_new_user):
        _, create_response = create_new_user
        token = create_response.json()["accessToken"]
        headers = {'Authorization': token}

        with allure.step("Отправить POST запрос для создания заказа без ингредиентов"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_ORDER,
                headers=headers,
                data=Ingredients.incorrect_ingredients_data_without_filling,
            )

        with allure.step("Проверить ответ создания заказа без ингредиентов"):
            assert response.status_code == StatusCode.BAD_REQUEST
            assert response.json().get("success") is False

    @allure.title('Проверка создания заказа авторизованным пользователем с несуществующими ингредиентами')
    @allure.description('''
                        1. Отправляем запрос на создание пользователя;
                        2. Отправляем запрос на создание заказа с невалидным хешем ингредиентов с авторизацией;
                        3. Проверяем ответ.
                        ''')
    def test_create_order_whith_incorrect_ingredients_is_not_created(self, create_new_user):
        _, create_response = create_new_user
        token = create_response.json()["accessToken"]
        headers = {'Authorization': token}

        with allure.step("Отправить POST запрос для создания заказа с невалидными ингредиентами"):
            response = requests.post(
                URL.main_url + Endpoints.CREATE_ORDER,
                headers=headers,
                data=Ingredients.incorrect_ingredients_data_hash,
            )

        with allure.step("Проверить ответ создания заказа с невалидными ингредиентами"):
            assert response.status_code == StatusCode.INTERNAL_SERVER_ERROR
            assert TextResponse.SERVER_ERROR in response.text
