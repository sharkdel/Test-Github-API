import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TestGithubAPI():
    """Создание и удаление репозитория на github"""

    base_url = "https://api.github.com/"  # Баззовый url
    path = "user/repos"
    path_get = f"users/{os.getenv('user_name')}/repos"
    path_delete = f"repos/{os.getenv('user_name')}/{os.getenv('reponame')}"

    headers = {
        "authorization": "Bearer {}".format(os.getenv('token'))
    }

    data = {
        "name": os.getenv('reponame'),
        "description": "Создано API",
        "homepage": "https://github.com",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    repositories = []

    def test_create_repository(self):
        """Создание репозитория"""

        print("\n Создание репозитория")
        """Получаем список репозиториев. GET"""
        response_get = requests.get(self.base_url + self.path_get, auth=("os.getenv('user_name')", os.getenv('token')))
        assert response_get.status_code == 200, 'ОШИБКА, Статус-код не совпадает'
        print("Статус код: ", response_get.status_code)
        print(self.base_url + self.path_get)
        all_repositories = response_get.json()  # Получаем список репозиториев пользователя

        counter = len(all_repositories)     # Кол-во репозиториев
        print("Всего репозиториев: ", counter)     # кол-во репозиториев
        for i in range(counter):
            print(all_repositories[i]['name'], end=" ")

        """Создание нового репозитория. POST"""
        response_post = requests.post(self.base_url + self.path, headers=self.headers, json=self.data)
        new_repository = response_post.json()  # Получаем репозиторий пользователя
        assert response_post.status_code == 201, 'ОШИБКА, Статус-код не совпадает'
        print("\n", "Статус код: ", response_post.status_code)
        assert os.getenv('reponame') in new_repository['name'], "Название не совпадает"
        print("Создан новый репозиторий: ", new_repository['name'])

        """Проверка, что репозиториев стало больше"""
        response_get = requests.get(self.base_url + self.path_get, auth=("os.getenv('user_name')", os.getenv('token')))
        assert response_get.status_code == 200, 'ОШИБКА, Статус-код не совпадает'
        print("Статус код: ", response_get.status_code)
        all_repositories = response_get.json()  # Получаем список репозиториев пользователя
        print("Стало репозиториев: ", len(all_repositories))     # кол-во репозиториев
        assert counter + 1 == len(all_repositories), "Кол-во репозиториев не изменилось"
        for i in range(len(all_repositories)):
            self.repositories.append(all_repositories[i]['name'])
        print(self.repositories)
        assert os.getenv('reponame') in self.repositories, "Репозитория нет в списке"
        print(os.getenv('reponame'), "есть в списке репозиториев")


    def test_delete_repository(self):
        """Удаление выбранного репозитория"""
        print("\n Удаление репозитория")
        """Получаем список репозиториев. GET"""
        response_get = requests.get(self.base_url + self.path_get, auth=("os.getenv('user_name')", os.getenv('token')))
        assert response_get.status_code == 200, 'ОШИБКА, Статус-код не совпадает'
        print("Статус код: ", response_get.status_code)
        print(self.base_url + self.path_get)
        all_repositories = response_get.json()  # Получаем список репозиториев пользователя

        counter = len(all_repositories)  # Кол-во репозиториев
        print("Всего репозиториев: ", counter)  # кол-во репозиториев
        for i in range(counter):
            print(all_repositories[i]['name'], end=" ")

        """Удаление репозитория. DELETE"""
        response_delete = requests.delete(self.base_url + self.path_delete, auth=("os.getenv('user_name')",
                                                                                  os.getenv('token')), json=self.data)
        assert response_delete.status_code == 204, 'ОШИБКА, Статус-код не совпадает'
        print("\n", "Статус код: ", response_delete.status_code)
        """Проверка, что репозитория больше нет"""
        response_get = requests.get(self.base_url + self.path_get, auth=("os.getenv('user_name')", os.getenv('token')))
        assert response_get.status_code == 200, 'ОШИБКА, Статус-код не совпадает'
        print("\n", "Статус код: ", response_get.status_code)
        after_delete = response_get.json()  # Получаем список репозиториев пользователя
        print("Стало репозиториев: ", len(after_delete))  # кол-во репозиториев
        assert len(after_delete) == len(all_repositories) - 1, "Кол-во репозиториев не изменилось"
        for i in range(len(after_delete)):
            print(all_repositories[i]['name'], end=" ")

