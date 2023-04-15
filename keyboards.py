from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button1 = KeyboardButton('Новый коктейль')
button2 = KeyboardButton('Посмотреть список своих коктейлей')
button3 = KeyboardButton('Удалить коктейль из списка')
buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2).insert(button3)
