import logging
import ephem


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler  
from handlers import greet_user,planet_go,newmoon,word_count,send_cat_picture,change_avatar,talk_to_me,get_contact,get_location

import settings




logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
)




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