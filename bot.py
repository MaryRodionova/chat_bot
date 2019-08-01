"""
Домашнее задание №1
Использование библиотек: ephem
* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход 
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите 
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите 
  бота отвечать, в каком созвездии сегодня находится планета.
"""
import logging
import ephem
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)


PROXY = {
    'proxy_url': 'socks5h://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {
        'username': 'learn', 
        'password': 'python'
    }
}


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)

def word_count(bot, update):
    user_text_word= update.message.text
    word_split=user_text_word.split()
    if len(word_split)>1:
        count_word=len(word_split)-1
    else:
         count_word='Введите фразу'   
    update.message.reply_text(count_word)

def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)
 
def planet_go(bot,update):
    user_text_planet= update.message.text
    planet_split=user_text_planet.split()
    planet_name=planet_split[1].capitalize()
    #print(planet)   

    today = datetime.datetime.today()
    today_st=today.strftime("%Y/%m/%d")

    planet=getattr(ephem,planet_name)(today_st)
    print (planet)
    const=ephem.constellation(planet)      
    update.message.reply_text(const)

def newmoon(bot,update):
    user_text_moon= update.message.texts
    moon_split=user_text_moon.split()
    moon_date=str(moon_split[1])  
    
    next_moon=ephem.next_full_moon(moon_date) 
    print(next_moon)  

    update.message.reply_text(next_moon)

def main():
    mybot = Updater("705952373:AAHroSOXqrgr0dySvq2oZxpHVavWwTL956g", request_kwargs=PROXY)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_go))
    dp.add_handler(CommandHandler("next_full_moon", newmoon))
    dp.add_handler(CommandHandler("wordcount", word_count))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    

    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()