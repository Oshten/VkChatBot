#! engoding = utf8

import logging, logging.config
from vk_api import vk_api, bot_longpoll
from random import randint
from log_config import bot_log_config

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py, change group_id and set token')


logging.config.dictConfig(bot_log_config)
log = logging.getLogger('bot')

class Bot:
    """
    Echo bot for group vk.com
    Use python 3.8
    """

    def __init__(self, token, group_id):
        '''

        :param token: sekret token for group vk.com.
        :param group_id: id for group vk.com
        '''
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoller = bot_longpoll.VkBotLongPoll(vk=self.vk, group_id=group_id, wait=60)
        self.base_names = []
        # TODO Добавить время отключения

    def run(self):
        '''Start bot'''
        for event in self.longpoller.listen():
            log.info('Получено событие %s' %event.type)
            if event.type == bot_longpoll.VkBotEventType.MESSAGE_TYPING_STATE:
                log.debug('Нам кто-то пишет')
                user_name = self._find_username(event)
                if user_name and not self._check_username(user_name=user_name):
                    log.debug('Приветствие пользователя')
                    self.event_processing(
                        message_answer=f'Тебя приветствую, падаван, {user_name}!',
                        event=event,
                        peer_id=event.object.from_id
                    )
            if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
                log.debug('Получено сообщение')
                message = event.message.text
                log.debug('Отправляем ответ')
                self.event_processing(
                    message_answer=self._find_message(
                        user_name=user_name,
                        message=message
                    ),
                    event=event,
                    peer_id=event.message.peer_id
                )
            else:
                log.info('Не умею обрабатывать такие события - %s' %event.type)


    def event_processing(self, message_answer, event, peer_id):
        '''

        :param message_answer: message to send
        :param event: VkBotEvent(object)
        :param peer_id: id recipient in vk.com
        :return: users name
        '''
        try:
            self.vk.method(
                method='messages.send',
                values={
                    'message' : message_answer,
                    'random_id' : randint(1, 2**50),
                    'peer_id' : peer_id
                }
            )
            log.info('Отправляю сообщение - %s' %message_answer)
        except Exception:
            log.exception('Что-то не то мы делаем')

    def _find_username(self, event):
        '''

        :param event: VkBotEvent(object)
        :return: users name
        '''
        users_info = self.vk.method(method='users.get', values={'user_ids': event.object.from_id})
        user_name = None
        try:
            user_name = users_info[0]['first_name']
            user_name += ' ' + users_info[0]['last_name']
            log.debug('Определяем имя и фамилию пользователя - %s' %user_name)
        except KeyError:
            if user_name:
                log.debug('Фамилия не указана')
            else:
                log.debug('Имя и фамилия не указаны')
        return user_name

    def _check_username(self, user_name):
        '''

        :param user_name: users name
        :return: true if user known or false if user don't known
        '''
        if user_name in self.base_names:
            log.debug('Пользователь в базе присутствует')
            return True
        elif user_name:
            self.base_names.append(user_name)
            log.debug('Добавляем нового пользователя')
            return False
        log.debug('Пользователь не определен')
        return False

    def _find_message(self, user_name, message):
        '''

        :param user_name: users name
        :param message: users message
        :return: message to send
        '''
        result_check_username = self._check_username(user_name=user_name)
        result_check_message = self._check_message(message=message)
        if result_check_username:
            if not result_check_message:
                get_message = message.strip().replace(',', '').replace('.', '').replace('бот', '').replace('!', '')
                log.debug('Сообщение пользователя - %s' %get_message)
                message_list = get_message.lower().split(' ')[::-1]
                message_list[0] = message_list[0].title()
                messege_answer = ' '.join(message_list) + ', падаван.'
                log.debug('Сформированно сообщение - %s' %messege_answer)
            elif result_check_message == 'question_who':
                log.debug('Пользователь интересуется ботом')
                messege_answer = 'Йодабот я, падаван.'
        elif not user_name:
            log.debug('Имя не определено')
            messege_answer = 'Темны мысли твои. Кто ты?'
        else:
            log.debug('Приветствует первым')
            message_answer = f'Тебя приветствую, падаван, {user_name}!'
        return messege_answer

    def _check_message(self, message):
        '''

        :param message: users message
        :return: answer to question 'who is you' or false
        '''
        if 'кто' and 'ты' in message.lower():
            return 'question_who'
        return False



if __name__ == '__main__':
    bot = Bot(token=settings.TOKEN, group_id=settings.GROP_ID)
    bot.run()

