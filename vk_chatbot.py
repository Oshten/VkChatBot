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
        self.base_names = []
        # TODO Добавить время отключения

    def run(self):
        for event in self.longpoller.listen():
            if event.type == bot_longpoll.VkBotEventType.MESSAGE_TYPING_STATE:
                print(event)
                user_name = self._find_username(event)
                if user_name:
                    self.event_processing(
                        message_answer=f'Тебя приветствую, падаван, {user_name}!',
                        event=event
                    )
            if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
                message = event.message.text
                self.event_processing(
                    message_answer='sss',
                    event=event
                )
            else:
                print('Не умею обрабатывать такие события', event.type)


    def event_processing(self, message_answer, event):
        try:
            self.vk.method(
                method='messages.send',
                values={
                    'message' : message_answer,
                    'random_id' : randint(1, 2**50),
                    'user_id' : event.object.user_id
                }
            )
        except Exception as exc:
            print('Что-то не то мы делаем', exc)

    def _find_username(self, event):
        users_info = self.vk.method(method='users.get', values={'user_ids': event.object.from_id})
        users_name = None
        try:
            user_name = users_info[0]['first_name']
            user_name += ' ' + users_info[0]['last_name']
        except KeyError:
            if user_name:
                print ('Фамилия не указана')
            else:
                print('Имя и фамилия не указаны')
        return user_name

    def _check_username(self, user_name):
        if user_name in self.base_names:
            return True
        elif user_name:
            self.base_names.append(user_name)
            return False
        return False

    def _find_message(self, user_name, message):
        result_check_username = self._check_username(user_name=user_name)
        result_check_message = self._check_message(message=message)
        if result_check_username:
            if not result_check_message:
                get_message = message.strip().replace(',', '').replace('.', '').replace('бот', '')
                message_list = get_message.lower().split(' ')[::-1]
                message_list[0] = message_list[0].title()
                messege_answer = ' '.join(message_list) + ', падаван.'
            elif result_check_message == 'question_who':
                messege_answer = 'Йодабот я, падаван.'
        elif not user_name:
            messege_answer = 'Темны мысли твои. Кто ты?'
        else:
            message_answer = f'Тебя приветствую, падаван, {user_name}!'
        return messege_answer

    def _check_message(self, message):
        if 'кто' and 'ты' in message.lower():
            return 'question_who'
        return False



if __name__ == '__main__':
    bot = Bot(token=token, group_id=group_id)
    bot.run()

