from aiogram import Bot, Dispatcher, executor, types
from numpy.random import randint
from nekot import TOKEN

START_MSG = "привет, коллега, напиши что у тебя есть, что ты хочешь, формат можешь подглядеть"
FORMAT_MSG = "Ингредиенты:\nвино с водой\nсок\nсидр\nКачества:\nсладко\nне крепко\nкисло\n\nкоктейль не понравился? удали рецепт сообщением \"*номер*!\""
END_MSG1 = "интересный вкус, а вот и рецепт"
END_MSG2 = "оки доки, босс, вот твой коктейль"
END_MSG3 = "коктейли, не можешь с ними, не можешь без них"
NUM_REC = "номер твоего коктейля "
NUM_REMOVE = "удалил, чекай братик"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
dict_of_cockts = {}
num_dict = {}
cock_num = 0
wrong_nums = []


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(START_MSG)


@dp.message_handler(commands=['format'])
async def format_handler(message: types.Message):
    await message.answer(FORMAT_MSG)


@dp.message_handler()
async def send_handler(message: types.Message):
    global cock_num
    text = message.text

    if text.isdigit() and int(text) <= cock_num and wrong_nums.count(int(text)) == 0:
        await message.answer(dict_of_cockts[num_dict[int(text)]])
        await message.answer(END_MSG3)

    elif text[:-1].isdigit() and text[-1:] == "!" and int(text[:-1]) <= cock_num:
        dict_of_cockts.pop(num_dict[int(text[:-1])])
        wrong_nums.append(int(text[:-1]))
        await message.answer(NUM_REMOVE)

    elif text.count(':') != 2:
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
                help_int = randint(1, 6)
                sum_int += help_int
                prop.append(help_int)
            for i in range(1, len(ings)-1):
                if len(str(prop[i-1]/sum_int)) < 3:
                    added = str(prop[i-1]/sum_int)
                else:
                    added = str(prop[i-1])+"/"+str(sum_int)
                ans += str(ings[i])+" : "+added+"\n"
            dict_of_cockts[tuple(ings)] = ans
            cock_num += 1
            num_dict[cock_num] = tuple(ings)

        msg_num = randint(1, 4)

        if msg_num == 1:
            await message.answer(END_MSG1)

        elif msg_num == 2:
            await message.answer(END_MSG2)

        else:
            await message.answer(END_MSG3)

        await message.answer(ans)
        await message.answer(NUM_REC + str(cock_num))


if __name__ == "__main__":
    executor.start_polling(dp)
