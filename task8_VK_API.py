
import os
import requests
import json
from dotenv import load_dotenv

class VK_API:
    def __init__(self, id_or_url: str, vk_token: str) -> None:
        self.response = None
        self.VK_tkn = vk_token

        user_info = requests.get("https://api.vk.com/method/users.get", params={
            "access_token": self.VK_tkn,
            "v": "8.131",
            "user_ids": id_or_url,
            "name_case": "gen"
        })

        try:
            user_info_json = user_info.json()
            if "response" in user_info_json and user_info_json["response"]:
                self.user_id = user_info_json["response"][0]["id"]
                self.user_info = user_info_json["response"][0]
            else:
                print(f"Error receiving user data: {user_info_json.get('error', 'Unknown error')}")
                raise ValueError("No user found or API error") #Более конкретная ошибка
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            print(f"Raw response: {user_info.text}") #Полезно для отладки
            raise
        except (KeyError, IndexError) as e:
            print(f"Error accessing user data: {e}")
            print(f"Raw response: {user_info_json}") #Полезно для отладки
            raise
        except ValueError as e:
            raise # Передаем ошибку дальше

    # метод для вывода списка друзей пользователей VK
    def print_friends(self) -> None:
        # Если ответ на запрос получен
        if self.response:
            # Выводится информация о друзьях пользователя
            print(f"\nДрузья {self.user_info['first_name']} {self.user_info['last_name']}:  \n")
            # Итерация по списку друзей пользователя
            counter = 1
            for i in self.response.json()["response"]["items"]:
                # Выводится информация о каждом друге
                print(f'{counter})\t{i["first_name"]} {i["last_name"]} - id: {i["id"]}')
                counter += 1
        # Если ответ на запрос не получен
        else:
            # Отправляется новый запрос на получение списка друзей пользователя
            self.response = requests.get("https://api.vk.com/method/friends.get", params={
                "access_token": self.VK_tkn,
                "v": "8.131",
                "user_id": self.user_id,
                "fields": "city",
                "order": "name"
            })
            # Рекурсивный вызов
            self.print_friends()


def main():
    load_dotenv()
    vktoken = os.environ.get("VK_tkn")  # Получаем токен VK API из переменной окружения
    #print(f"VK_tkn: {vktoken}")
    name = input("input user_id or short_url: ")  # Получаем ID пользователя VK
    Api = VK_API(name, vktoken)
    Api.print_friends()


if __name__ == '__main__':
    main()
