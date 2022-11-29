from types import SimpleNamespace
from telebot import types
import emoji

def keyboard(*keys, row_width=2, resize_keyboard=True):
   markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
   button = map(types.KeyboardButton, keys)
   markup.add(*button)
   return markup

keys = SimpleNamespace(
    main='main',
    hi='hi:waving_hand_light_skin_tone:'
)

mykeyboard = SimpleNamespace(
    first=keyboard(keys.main, emoji.emojize(keys.hi))
    )

