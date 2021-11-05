import logging
from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotEvent

from vk_chatbot import Bot
from raw_event import RAW_EVENT_MESSAGE_NEW, RAW_EVENT_MESSAGE_TYPING_STATE, INFO_USERS


class Test_bot(TestCase):
    logging.disable(logging.ERROR)

    def test_run_event_mesage_typing_state(self):  # Проверка что функция run вызывает следующую функцию
        count = 5
        event = Mock()
        event.type = 'message_typing_state'
        events = [event]*count       # [{}, {}, ...]
        longpoller_mock = Mock(return_value=events)
        longpoller_listen_mock = Mock()
        longpoller_listen_mock.listen = longpoller_mock
        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll', return_value=longpoller_listen_mock):
                with patch('vk_chatbot.bot_longpoll.VkBotEventType') as vk_bot_event_type:
                    bot = Bot('', '')
                    vk_bot_event_type.MESSAGE_TYPING_STATE = 'message_typing_state'
                    bot._find_username = Mock(return_value='Вася Пупкин')
                    bot._check_username = Mock(return_value=False)
                    bot.event_processing = Mock()
                    bot.run()

                    bot.event_processing.assert_called()
                    bot._find_username.assert_called_with(event)
                    self.assertEqual(bot.event_processing.call_count, count)


    def test_run_message_new(self):  # Проверка что функция run вызывает следующую функцию
        count = 5
        event = Mock()
        event.type = 'message_new'
        event.message = Mock()
        event.message.text = 'Привет'
        events = [event]*count       # [{}, {}, ...]
        longpoller_mock = Mock(return_value=events)
        longpoller_listen_mock = Mock()
        longpoller_listen_mock.listen = longpoller_mock
        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll', return_value=longpoller_listen_mock):
                with patch('vk_chatbot.bot_longpoll.VkBotEventType') as vk_bot_event_type:
                    bot = Bot('', '')
                    vk_bot_event_type.MESSAGE_NEW = 'message_new'
                    bot._find_message = Mock()
                    bot._find_username = Mock(return_value='Вася Пупкин')
                    bot.event_processing = Mock()
                    bot.run()

                    bot.event_processing.assert_called()
                    self.assertEqual(bot.event_processing.call_count, count)


    def test_run_all_message(self):  # Проверка что функция run не вызывает следующую функцию
        event_types = [
            'message_reply',
            'message_edit',
            'message_event',
            'message_allow',
            'message_deny',
            'photo_new',
        ]
        events = []
        for type in event_types:
            event = Mock()
            event.type = type
            events.append(event)
        longpoller_mock = Mock(return_value=events)
        longpoller_listen_mock = Mock()
        longpoller_listen_mock.listen = longpoller_mock
        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll', return_value=longpoller_listen_mock):
                with patch('vk_chatbot.bot_longpoll.VkBotEventType') as vk_bot_event_type:
                    bot = Bot('', '')
                    vk_bot_event_type.MESSAGE_NEW = 'message_new'
                    vk_bot_event_type.MESSAGE_TYPING_STATE = 'message_typing_state'
                    bot.event_processing = Mock()
                    bot.run()

                    self.assertEqual(bot.event_processing.assert_not_called(), None)


    def test_event_processing(self):
        message_answer = 'Привет, падаван'
        peer_id = 38123382

        events = [
            VkBotEvent(RAW_EVENT_MESSAGE_NEW),
            VkBotEvent(RAW_EVENT_MESSAGE_TYPING_STATE)
        ]

        with patch('vk_chatbot.vk_api.VkApi') as vk:
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                vk.method = Mock()
                for event in events:
                    bot.event_processing(message_answer=message_answer, event=event, peer_id=peer_id)

                    bot.vk.method.assert_called_with(
                        method='messages.send',
                        values={
                            'message': message_answer,
                            'random_id': ANY,
                            'peer_id': peer_id
                        }
                    )
                bot.vk.method.assert_called()
                self.assertEqual(bot.vk.method.call_count, len(events))


    def test_find_username_start_request(self):
        events = [
            VkBotEvent(RAW_EVENT_MESSAGE_NEW),
            VkBotEvent(RAW_EVENT_MESSAGE_TYPING_STATE),
        ]
        values = [
            {'user_ids': VkBotEvent(RAW_EVENT_MESSAGE_NEW).object.message['from_id']},
            {'user_ids': VkBotEvent(RAW_EVENT_MESSAGE_TYPING_STATE).object.from_id}
        ]

        with patch('vk_chatbot.vk_api.VkApi') as vk:
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                vk.method = Mock()

                for event, value in zip(events, values):
                    bot._find_username(event)
                    bot.vk.method.assert_called_with(method='users.get', values=value)

                bot.vk.method.assert_called()
                self.assertEqual(bot.vk.method.call_count, len(events))


    def test_find_full_username(self):
        event = VkBotEvent(RAW_EVENT_MESSAGE_NEW)

        with patch('vk_chatbot.vk_api.VkApi') as vk:
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                bot.vk.method = Mock(return_value=INFO_USERS[0])

                user_name = bot._find_username(event)
                self.assertEqual(user_name, 'Руслан Ильин')


    def test_find_first_username(self):
        event = VkBotEvent(RAW_EVENT_MESSAGE_NEW)

        with patch('vk_chatbot.vk_api.VkApi') as vk:
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                bot.vk.method = Mock(return_value=INFO_USERS[1])

                user_name = bot._find_username(event)
                self.assertEqual(user_name, 'Руслан')


    def test_find_not_username(self):
        event = VkBotEvent(RAW_EVENT_MESSAGE_NEW)

        with patch('vk_chatbot.vk_api.VkApi') as vk:
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                bot.vk.method = Mock(return_value=INFO_USERS[2])

                user_name = bot._find_username(event)
                self.assertEqual(user_name, None)


    def test_check_username(self):

        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                resalt = bot._check_username()
                self.assertEqual(resalt, False)
                self.assertEqual(len(bot.base_names), 0)

                bot.user_name = 'Вася Пупкин'
                resalt = bot._check_username()
                self.assertEqual(resalt, False)
                self.assertEqual(len(bot.base_names), 1)

                resalt = bot._check_username()
                self.assertEqual(resalt, True)

    def test_find_message(self):

        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll'):
                bot = Bot('', '')
                resalt = bot._find_message(message='Привет, бот.')
                self.assertEqual(resalt, 'Темны мысли твои. Кто ты?')

                bot.user_name = 'Вася Пупкин'
                resalt = bot._find_message(message='Привет, бот.')
                self.assertEqual(resalt, f'Тебя приветствую, падаван, {bot.user_name}!')

                resalt = bot._find_message(message='Началась клоническая война')
                self.assertEqual(resalt, 'Война клоническая началась, падаван.')



























