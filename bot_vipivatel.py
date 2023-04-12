from aiogram import Bot, Dispatcher, executor, types
from numpy.random import randint
from nekot import TOKEN

START_MSG = "привет, коллега, напиши что у тебя есть, что ты хочешь, формат можешь подглядеть"
FORMAT_MSG = "Ингредиенты:\nвино с водой\nсок\nсидр\nКачества:\nсладко\nне крепко\nкисло"
END_MSG = "интересный вкус, а вот и рецепт"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
dict_of_cockts = {}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(START_MSG)


@dp.message_handler(commands=['format'])
async def format_handler(message: types.Message):
    await message.answer(FORMAT_MSG)


@dp.message_handler()
async def send_handler(message: types.Message):
    text = message.text
    if text.count(':') != 2:
        await message.answer("wrong door")
    else:
        inp = str(text).split(':')
        ings = inp[1].split('\n')
        fs = inp[2].split('\n')
        ans = ""
        prop = []
        sum_int = 0
        if tuple(ings) in dict_of_cockts:
            ans = dict_of_cockts[tuple(ings)]
        else:
            for i in range(len(ings)-2):
                help_int = randint(1, 10)
                sum_int += help_int
                prop.append(help_int)
            for i in range(1, len(ings)-1):
                if len(str(prop[i-1]/sum_int)) < 3:
                    added = str(prop[i-1]/sum_int)
                else:
                    added = str(prop[i-1])+"/"+str(sum_int)
                ans += str(ings[i])+" : "+added+"\n"
                dict_of_cockts[tuple(ings)] = ans
        await message.answer(END_MSG)
        await message.answer(ans)


if __name__ == "__main__":
    executor.start_polling(dp)
