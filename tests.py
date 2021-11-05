import logging
from unittest import TestCase
from unittest.mock import patch, Mock

from vk_chatbot import Bot


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



