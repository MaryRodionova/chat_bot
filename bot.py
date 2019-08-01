"""
"""

from glob import glob
import logging
import ephem
from datetime import datetime
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler  

import settings



logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)




def greet_user(bot, update,user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = 'Привет {}'.format(emo)
    
    
    update.message.reply_text(text, reply_markup= get_keyboard())
    

def word_count(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text_word= update.message.text
    word_split=user_text_word.split()
    if len(word_split)>1:
        count_word=len(word_split)-1
    else:
         count_word='Введите фразу'   
    update.message.reply_text(count_word, reply_markup=get_keyboard())

def talk_to_me(bot, update , user_data):
    emo = get_user_emo(user_data)
    user_text = "Привет {} {} ! Ты написал: {}".format(update.message.chat.first_name, user_data ['emo'], 
                update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)

    update.message.reply_text(user_text, reply_markup=get_keyboard())
 
def planet_go(bot,update):
    user_text_planet= update.message.text
    planet_split=user_text_planet.split()
    planet_name=planet_split[1].capitalize()
    #print(planet)   

    today = datetime.datetime.today()
    today_st=today.strftime("%Y/%m/%d")

    planet=getattr(ephem,planet_name)(today_st)
    #print (planet)
    const=ephem.constellation(planet)      
    update.message.reply_text(const, reply_markup=get_keyboard())

def newmoon(bot,update):
    user_text_moon= update.message.texts
    moon_split=user_text_moon.split()
    moon_date=str(moon_split[1])  
    
    next_moon=ephem.next_full_moon(moon_date) 
    print(next_moon)  

    update.message.reply_text(next_moon, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    emo = get_user_emo(user_data)
    cat_list = glob('images/cat*.jp*g') #шаблон для выбора
    cat_pic = choice(cat_list) #случайное имя файла
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())   

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(emo),reply_markup=get_keyboard() ) 

def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Спасибо {}'.format(get_avatar(user_data)), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Спасибо {}'.format(get_avatar(user_data)), reply_markup=get_keyboard())

def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)

    my_keyboard = ReplyKeyboardMarkup([
                                    ['Прислать котика', 'Сменить аватарку'],
                                    [contact_button, location_button]
                                    ], resize_keyboard=True
                                    )
    return my_keyboard

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", planet_go))
    dp.add_handler(CommandHandler("next_full_moon", newmoon))
    dp.add_handler(CommandHandler("wordcount", word_count, pass_user_data=True))
   
    dp.add_handler(CommandHandler("cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me ,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
       
    

    mybot.start_polling()
    mybot.idle()
       

if __name__ == "__main__":
    main()