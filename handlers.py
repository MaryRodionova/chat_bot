from glob import glob

import logging
from random import choice
from datetime import datetime

from utils import get_keyboard,get_user_emo

import settings
import ephem

def greet_user(bot, update, user_data):
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
    #print(next_moon)  

    update.message.reply_text(next_moon, reply_markup=get_keyboard())



    




def send_cat_picture(bot, update, user_data):
    emo = get_user_emo(user_data)
    cat_list = glob('images/cat*.jp*g') #шаблон для выбора
    cat_pic = choice(cat_list) #случайное имя файла
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())   



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

