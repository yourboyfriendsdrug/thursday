#импорт библиотек



TOKEN = ""

HELP = """
help  - вывод списка команд
add   - добавление задачи
show  - показать все задачи
done  - задача выполнена
"""
todo = {}

print("Привет! Введи команду help для вывода списка команд")

while True:
  userAnswer = input("Введите команду:\n")

  if userAnswer == "add":
    userDate = input( "Введите дату:\n" )
    userTask = input( "Что нужно сделать?\n" )

    todo[ userDate ] = userTask
    print(f"На {userDate} число добавлена задача '{userTask}'")
  elif userAnswer == "help":
    print(HELP)
  elif userAnswer == "show":
    for date in todo.keys():
      print( f"[ {date} ] - {todo[date]}")
  elif userAnswer == "done":
    print("Работает!")
  elif userAnswer == "exit":
    break
  else:
    print("Error. Нет такой команды")
    print("Введиет help для вывода списка команд")