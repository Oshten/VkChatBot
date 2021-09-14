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
        print(message)
        # metod = self.vk.get_api()
        try:
            self.vk.method(
                method='messages.send',
                values={
                    'message' : message,
                    'random_id' : randint(1, 2**50),
                    'peer_id' : event.message.peer_id
                }
            )
        except Exception as exc:
            print('Что-то не то мы делаем', exc)




if __name__ == '__main__':
    bot = Bot(token=token, group_id=group_id)
    bot.run()

