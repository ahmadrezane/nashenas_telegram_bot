import emoji

from loguru import logger

from src.bot import bot
from src.constant import mykeyboard, keys, states
from src.db import db
from src.filters import IsAdmin

# flake8: noqa on a line by itself

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
      @self.bot.message_handler(commands=['start', 'help'])
      def start(message):
         self.bot.reply_to(message, 'Hi how can i help you', reply_markup=mykeyboard.main)
         db.users.update_one(
            {'chat_id': message.chat.id},
            {'$set': message.json},
            upsert=True
            )
         self.update_state(message.chat.id, states.idle)

      @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
      def random_connect(message):
         self.bot.send_message(
            message.chat.id,
            '<strong>Connecting to a random stranger...</strong>',
            reply_markup=mykeyboard.second
            )
         self.update_state(message.chat.id, states.random_connect)
         other_user = db.users.find_one(
            {
               'state': states.random_connect,
               'chat_id': {'$ne': message.chat.id}
            }
         )

         if not other_user:
            return
         #update other_user state
         self.update_state(other_user['chat']['id'], states.connected)
         self.bot.send_message(
            other_user['chat']['id'],
            f"you are connected to {message.chat.first_name} ..."
            )

         #update user state
         self.update_state(message.chat.id, states.connected)
         self.bot.send_message(
            message.chat.id,
          f'you are connected to {other_user["chat"]["first_name"]} ....'
          )

         #store connected user
         db.users.update_one(
            {'chat_id': message.chat.id},
            {'$set': {'connected_to':other_user['chat']['id']}}
         )

         db.users.update_one(
            {'chat_id': other_user['chat']['id']},
            {'$set': {'connected_to':message.chat.id}}
         )

      @self.bot.message_handler(regexp=emoji.emojize(keys.stop))
      def stop(message):
         self.bot.send_message(
            message.chat.id,
             'stop connection',
              reply_markup=mykeyboard.main
              )
         self.update_state(message.chat.id, states.stop)

         # update other user state
         connected_to = db.users.find_one(
            {'chat_id':message.chat.id}
         )['connected_to']

         if not connected_to:
            return
         #disconnect users
         self.bot.send_message(connected_to, f'{message.chat.first_name} leave the chat')

         self.update_state(connected_to, states.stop)

         # remove connected users
         db.users.update_one(
            {'chat_id': message.chat.id},
            {'$set': {'connected_to': None }}
         )

         db.users.update_one(
            {'chat_id':connected_to},
            {'$set': {'connected_to': None}}
         )


      @self.bot.message_handler(is_chat_admin=True)
      def is_admin(message):
         self.bot.send_message(message.chat.id, 'oh you are the boss and admin of this group')

      @self.bot.message_handler(func=lambda message:True)
      def echo_all(message):
         """"
         echo message to other connected user
         """
         
            user = db.users.find_one(
               {'chat_id': message.chat.id}
            )
            if (not user) (user['state'] != states.connected) or (user['connected_to'] == None):
               return

            self.bot.send_message(user['connected_to'], message.text)

   def send_message(self, chat_id, text, reply_markup=None, emojize=True):
      if emojize:
         text = emoji.emojize(text)
      self.bot.send_message(chat_id, text, reply_markup=reply_markup)

   def update_state(self, chat_id, state):
      """
      update user state
      """
      db.users.update_one(
         {'chat_id': chat_id},
         {'$set': {'state': state}}
      )





if __name__ == '__main__':
   bot = Bot(telebot=bot)


