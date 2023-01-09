from dotenv import find_dotenv, load_dotenv
import os


if not find_dotenv():
    exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('start', 'Запустить бота'),
    ('help', 'Вывести справку'),
    ('survey', 'Опрос'),
    ('low', 'Поиск по самому маленькому значению заданного параметра'),
    ('high', 'Поиск по самому большому значению заданного параметра'),
    ('custom', 'Поиск по пользовательским значениям заданного параметра'),
    ('history', 'Вывод последних 10 запросов')
)




