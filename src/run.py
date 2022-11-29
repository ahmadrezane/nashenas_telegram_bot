import emoji
from loguru import logger

from src.bot import bot
from src.constant import mykeyboard
from src.filters import IsAdmin
from src.utils.io import read_json, write_json


class Bot:
   def __init__(self, telebot):
      self.bot = telebot

      #add custom filters
      self.bot.add_custom_filter(IsAdmin())

      #register handlers
      self.handlers()

      #run bot
      logger.info('Bot is running....')
      self.bot.infinity_polling()

   def handlers(self):

      @self.bot.message_handler(is_chat_admin=True)
      def is_admin(message):
         self.bot.send_message(message.chat.id, 'oh you are the boss and admin of this group')
      @self.bot.message_handler(func=lambda message:True)
      def echo_all(message):
            self.send_message(message.chat.id,
             message.text,
              reply_markup=mykeyboard.first
              )
            print(emoji.demojize(message.text))
   def send_message(self, chat_id, text, reply_markup=None, emojize=True):
      if emojize:
         text = emoji.emojize(text)
      self.bot.send_message(chat_id, text, reply_markup=reply_markup)






if __name__ == '__main__':
   bot = Bot(telebot=bot)
   bot.run()

