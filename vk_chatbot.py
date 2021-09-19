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
            if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
                self.event_processing(event=event)
            else:
                print('Не умею обрабатывать такие события', event.type)


    def event_processing(self, event):
        message = event.message.text
        try:
            user_name, user_lastname, answer = self._find_username(event)
            if answer:
                if user_name:
                    message_answeer = f'Тебя приветствую, падаван, {user_name}!'
                else:
                    message_answeer = 'Тебя приветствую, падаван!\nТемны мысли твои. Кто ты?'
            else:
                message_answeer = f'Тебя приветствую, падаван, {user_name} {user_lastname}!'

            self.vk.method(
                method='messages.send',
                values={
                    'message' : message_answeer,
                    'random_id' : randint(1, 2**50),
                    'peer_id' : event.message.peer_id
                }
            )
        except Exception as exc:
            print('Что-то не то мы делаем', exc)

    def _find_username(self, event):
        users_info = self.vk.method(method='users.get', values={'user_ids': event.message.from_id})
        users_name, user_lastname, answer = None, None, None
        try:
            user_name = users_info[0]['first_name']
            user_lastname = users_info[0]['last_name']
        except KeyError:
            answer = 'Кто ты, падаван?'
        return user_lastname, user_name, answer


if __name__ == '__main__':
    bot = Bot(token=token, group_id=group_id)
    bot.run()

