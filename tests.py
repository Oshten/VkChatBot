from unittest import TestCase
from unittest.mock import patch, Mock

from vk_chatbot import Bot


class Test_bot(TestCase):

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


    def test_run_start(self):  # Проверка что функция run вызывает следующую функцию
        count = 5
        event = Mock()
        event.type = 'message_new'
        events = [event]*count       # [{}, {}, ...]
        longpoller_mock = Mock(return_value=events)
        longpoller_listen_mock = Mock()
        longpoller_listen_mock.listen = longpoller_mock
        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.bot_longpoll.VkBotLongPoll', return_value=longpoller_listen_mock):
                with patch('vk_chatbot.bot_longpoll.VkBotEventType') as vk_bot_event_type:
                    bot = Bot('', '')
                    vk_bot_event_type.MESSAGE_NEW = 'message_new'
                    bot._find_message = Mock(user_name='Вася Пупкин', return_value='Привет')
                    bot.event_processing = Mock()
                    bot.run()

                    bot.event_processing.assert_called()
                    self.assertEqual(bot.event_processing.call_count, count)



