from types import SimpleNamespace
from telebot import types
import emoji

def keyboard (*keys, row_width=2, resize_keyboard=True):
   markup = types.ReplyKeyboardMarkup(
    row_width=row_width,
    resize_keyboard=resize_keyboard
    )
   button = map(types.KeyboardButton, keys)
   markup.add(*button)
   return markup

keys = SimpleNamespace(
    random_connect='Random connect:busts_in_silhouette:',
    setting='Setting:gear:',
    stop='Stop connecting:red_circle:'
)

mykeyboard = SimpleNamespace(
    main=keyboard(emoji.emojize(keys.random_connect),
    emoji.emojize(keys.setting)),
    second=keyboard(emoji.emojize(keys.stop))
)

states = SimpleNamespace(
    idle='IDLE',
    random_connect='RANDOM_CONNECT',
    stop='STOP',
    connected='CONNECTED'
)
