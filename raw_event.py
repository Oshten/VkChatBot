'''
Задаем объект raw для создания event при тестировании
'''

RAW_EVENT_MESSAGE_NEW = {
            'type': 'message_new',
            'object': {
                'message': {
                    'date': 1636110485,
                    'from_id': 38123382,
                    'id': 348,
                    'out': 0,
                    'peer_id': 38123382,
                    'text': 'Привет, бот',
                    'attachments': [],
                    'conversation_message_id': 348,
                    'fwd_messages': [],
                    'important': False,
                    'is_hidden': False,
                    'random_id': 0
                },
                'client_info': {
                    'button_actions': [
                        'text',
                        'vkpay',
                        'open_app',
                        'location',
                        'open_link',
                        'callback',
                        'intent_subscribe',
                        'intent_unsubscribe'
                    ],
                    'keyboard': True,
                    'inline_keyboard': True,
                    'carousel': True,
                    'lang_id': 0
                }
            },
            'group_id': 207094096,
            'event_id': '63a1e13c0398eea3a422d425459f096dc201145a'
        }

RAW_EVENT_MESSAGE_TYPING_STATE = {
    'type': 'message_typing_state',
    'object': {
        'state': 'typing',
        'from_id': 38123382,
        'to_id': -207094096
    },
    'group_id': 207094096,
    'event_id': 'b8271d0fabbaf0a4128a55a1c59cc72c10238f10'
}

'''Информация о пользователе'''

INFO_USERS = [
            [
                {
                    'first_name': 'Руслан',
                    'id': 38123382,
                    'last_name': 'Ильин',
                    'can_access_closed': True,
                    'is_closed': False
                }
            ],
            [
                {
                    'first_name': 'Руслан',
                    'id': 38123382,
                    'can_access_closed': True,
                    'is_closed': False
                }
            ],
            [
                {
                    'id': 38123382,
                    'can_access_closed': True,
                    'is_closed': False
                }
            ]
        ]