#! encoding = utf8

bot_log_config = {
    'version': 1,
    'formatters': {
        'stream_format': {
            'format': '%(levelname)s - %(message)s'
        },
        'consol_format': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%d-%m-%Y %H:%m'
        }
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'stream_format'
        },
        'consol_handler': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'consol_format',
            'filename': 'bot.log',
            'encoding': 'UTF8'
        }
    },
    'loggers': {
        'bot': {
            'handlers': [
                'stream_handler',
                'consol_handler'
            ],
            'level': 'DEBUG',
        }
    }
}
