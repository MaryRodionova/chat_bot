CatBot

========

CatBot - это бот для Telegram созданный с целью делать вашу жизнь лучше, присылая вам фотографии котиков.

Установка

----------

Создайте виртуальное окружение и активируйте его. Потом в виртуальном окружении выполните:

.. code-block:: text

    pip install -r requirements.txt


Положите картинки с котиками в папку images. Название файлов должно начинаться с cat, расширение .jpg , например cat1234.jpg

Настройка

----------

Создайте файл settings.py  и добавьте туда след.настройки:

.. code-block:: python


PROXY = {
    'proxy_url': 'socks5h://ВАШ_ПРОКСИ:1080',
    'urllib3_proxy_kwargs': {
        'username': 'ЛОГИН', 
        'password': 'ПАРОЛЬ'
    }
}


API_KEY="API ключ, который вы получили у BotFather"

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

Запуск

----------

 В активном виртуальном окружении выполните:

 .. code-block:: text
 
    python3 bot.py