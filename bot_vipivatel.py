from aiogram import Bot, Dispatcher, executor, types
from numpy.random import randint
import keyboards
from aiogram.types import ReplyKeyboardRemove

TOKEN = "5940727481:AAFBmQm2Dzu_8S7PXbUc6BbqSzhgZA_54AQ"

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
flag_ing = 0
flag_wish = 0
flag_delete = 0
ings = []
wishes = []


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    first_name = message.from_user.first_name
    await message.answer(
        f"Привет, {first_name}, давай я тебе кратко расскажу, что я умею:\n\nНовый коктейль - пишешь список своих ингредиентов, пишешь свои пожелания, а я даю тебе пропорции для коктейля твоей мечты\n\nПосмотреть список своих коктейлей - все коктейли, которые ты запрашивал у меня я храню, можешь посмотреть рецепты, если что\n\nУдалить коктейль из списка - ну тут и объяснять нечего, пишешь номер коктейля, этот коктейль из списка убираем",
        reply_markup=keyboards.buttons)


@dp.message_handler()
async def handler(message: types.Message):
    global flag_wish, flag_ing, flag_delete, cock_num, ings
    text = message.text
    if text == 'Новый коктейль':
        await message.answer("Ну давай создавать, вводи ингредиенты", reply_markup=ReplyKeyboardRemove())
        flag_ing = 1
    elif text == 'Посмотреть список своих коктейлей':
        if (len(dict_of_cockts) == 0):
            await message.answer("Нету у тебя рецептов\n", reply_markup=keyboards.buttons)
        else:
            await message.answer("Держи список\n", reply_markup=keyboards.buttons)
            i = 1
            ans = ""
            for value in dict_of_cockts.values():
                ans += f"Коктейль {i}:" + '\n' + value + '\n'
                i += 1
            await message.answer(ans)
    elif text == 'Удалить коктейль из списка':
        if len(dict_of_cockts) == 0:
            await message.answer("Кого удалять собрался? Рецептов то нет.\n", reply_markup=keyboards.buttons)
        else:
            i = 1
            ans = ""
            for value in dict_of_cockts.values():
                ans += f"Коктейль №{i}" + '\n' + value + '\n'
                i += 1
            await message.answer(ans)
            await message.answer("Кого удаляем?", reply_markup=ReplyKeyboardRemove())
            flag_delete = 1
    else:
        if flag_delete == 1:
            delet = int(str(text))
            j = 1
            for key in dict_of_cockts.keys():
                if j == delet:
                    dict_of_cockts.pop(key)
                    await message.answer(f"Успешно удалили, теперь нет того коктейля {delet}",
                                         reply_markup=keyboards.buttons)
                j += 1
            flag_delete = 0
        elif flag_wish == 1:
            wishes = str(text).split('\n')
            ans = ""
            prop = []
            sum_int = 0

            if tuple(ings) in dict_of_cockts:
                ans = dict_of_cockts[tuple(ings)]

            else:
                for i in range(len(ings)):
                    help_int = randint(1, 6)
                    sum_int += help_int
                    prop.append(help_int)

                for i in range(len(ings)):
                    if len(str(prop[i - 1] / sum_int)) < 3:
                        added = str(prop[i - 1] / sum_int)
                    else:
                        added = str(prop[i - 1]) + "/" + str(sum_int)
                    ans += str(ings[i]) + " : " + added + "\n"

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
            await message.answer(NUM_REC + str(cock_num), reply_markup=keyboards.buttons)
            wishes.clear()
            flag_wish = 0
            flag_ing = 0
        elif flag_ing == 1:
            ings.clear()
            ings = str(text).split('\n')
            flag_wish = 1
            await message.answer("а теперь пожелания", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Чё...", reply_markup=keyboards.buttons)


if __name__ == "__main__":
    executor.start_polling(dp)
