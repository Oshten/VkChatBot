#! engoding = utf8

from vk_api import vk_api, bot_longpoll
from random import randint
import _key

group_id = 207094096
token = _key._access_key

class Bot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoller = bot_longpoll.VkBotLongPoll(vk=self.vk, group_id=group_id, wait=60)

    def run(self):
        for event in self.longpoller.listen():
            if event.message:
                self.event_processing(event=event)
            else:
                print('Не умею обрабатывать такие события')


    def event_processing(self, event):
        message = event.message.text
        print(event)
        print(message)
        # metod = self.vk.get_api()
        try:
            users_info = self.vk.method(method='users.get', values={'user_ids' : event.message.from_id})
            user_name = users_info[0]['first_name']
            print(users_info)
            self.vk.method(
                method='messages.send',
                values={
                    'message' : f'Привет, {user_name}!',
                    'random_id' : randint(1, 2**50),
                    'peer_id' : event.message.peer_id
                }
            )
        except Exception as exc:
            print('Что-то не то мы делаем', exc)






if __name__ == '__main__':
    bot = Bot(token=token, group_id=group_id)
    bot.run()

