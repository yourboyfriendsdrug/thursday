from app import bot, dp
from aiogram.types import Message
from config import admin_id, todo, HELP
import time

command = 0
# 0 - пользователь ничего не выбрал
# 1 - ожидаем дату для добавления задачи
# 2 - ожидаем задачу для добавления в словарь
# 3 - ожидаем вариант отображения задач
# 4 - ожидание даты для вывода задачи

userDate, userTask = 0, 0

def checkDate(uDate):
    try:
        time.strptime(uDate, '%d.%m.%Y')
        return True
    except ValueError:
        return False

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен!")

@dp.message_handler(commands = "start")
async def start(message:Message):
    await message.answer(text = "Работает")

@dp.message_handler(commands = "add")
async def add(message:Message):
    global command
    await message.answer(text = "Введите дату в формате дд.мм.гггг")
    command = 1

@dp.message_handler(commands = "done")
async def done(message:Message):
    global command
    await message.answer(text = "Введите дату в формате дд.мм.гггг")
    command = 5

@dp.message_handler(commands = "help")
async def help(message:Message):
    await message.answer(text = HELP)

@dp.message_handler(commands = "show")
async def show(message:Message):
    global command
    await message.answer(text = "[ 0 ] - вывести все задачи\n[ 1 ] - задачи по дате")
    command = 3


@dp.message_handler()
async def inputText(message:Message):
    global userDate, userTask, command, todo

    if command == 1:
        userDate = message.text

        # проверка корректности ввода
        if checkDate(userDate) == False:
            await bot.send_message(message.chat.id, "Неверный формат даты")
            command = 0
            return
       # запрос что нужно сделать
        await message.answer("Что нужно сделать?")
        command = 2
    elif command == 2:
        userTask = message.text
        if userDate in todo:
            todo[userDate].append(userTask)
        else:
            todo[userDate]=userTask
        await message.answer(f"Добавлена '{userTask}' на {userDate}")
        command = 0
    elif command == 3:
        if message.text == "0":
            # сортируем ключи и проходимся по ним циклом
            for date in sorted( todo.keys() ):
                # получаем список задач и выводим каждую задачу на новой строке
                for task in todo[ date ]:
                    await message.answer(text = f"[{date}] - '{task}'")
        elif message.text == "1":
            await message.answer(text = "Введите дату в формате дд.мм.гггг")
            command = 4
        else:
            await message.answer(text = "Неизвестная комманда")
            command == 0
    elif command == 4:
        userDate = message.text

        # проверка корректности ввода
        if checkDate(userDate) == False:
            await bot.send_message(message.chat.id, "Неверный формат даты")
            command = 0
            return
        
        if userDate in todo:
            for task in todo[ userDate ]:
                await message.answer(text = f"[{userDate}] - '{task}'")
        command = 0
    elif command == 5:
        userDate = message.text

        # проверка корректности ввода
        if checkDate(userDate) == False:
            await bot.send_message(message.chat.id, "Неверный формат даты")
            command = 0
            return

        if  userDate in todo:
            if len( todo[ userDate ] ) > 1:
                await message.answer(text = "Какую задачу выполнили?")
                tmp = 1
                for task in todo[ userDate]:
                    await message.answer(text = f"[{tmp}] - '{task}'") 
                    tmp += 1
                command = 6
            else:
                await message.answer(text = f"Задача { todo.pop(userDate)[0] } - удалена")
        else:
            await message.answer(text = "На указанную дату нет задач")
            command = 0
    elif command == 6:
        tmp = todo[userDate]
        try:
            index = int(message.text) - 1
        except ValueError:
            await message.answer(text = "Не верный формат ввода")
            command = 0

        if len( tmp ) > index:
            await message.answer(text = f"Задача { tmp.pop(index) } - удалена")
            todo[ userDate ] = tmp
            command = 0
    else:
        await message.answer(text = "нет такой команды")
        await message.answer(text = "для вывода списка команд введите /help")


    