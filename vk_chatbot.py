#! engoding = utf8

from vk_api import vk_api, bot_longpoll
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
            print(event.message)


if __name__ == '__main__':
    bot = Bot(token=token, group_id=group_id)
    bot.run()

