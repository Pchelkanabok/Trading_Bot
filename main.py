from ver_1_0 import first_data
import datetime
import time

# from tkinter import Tk, Button, Menu, Entry
# from tkinter.ttk import Label

work_time, work_time_sko, flag = 0, 0, 0


def read_mas_in_file(name):  # Функция чтения массива из файла
    read_mass = []
    f = open("C:/QUIK_AD/Quik/lua/data/" + name + ".txt", "w+")
    # open(file="C:/QUIK_VTB/lua/data/1.txt", mode="r+", encoding="utf-8")
    for line in f:
        read_mass.append(*[int(x) for x in line.split()])
    f.close()
    return read_mass


def working_hours():
    global flag
    work_time_now = datetime.datetime.today()

    if str('10.10.00') < str(work_time_now.strftime("%H.%M.%S")) < str('13.55.00'):
        flag = 1
    elif str('14.10.00') < str(work_time_now.strftime("%H.%M.%S")) < str('17.30.00'):
        flag = 1
    else:
        flag = 0
    print(flag)
    return flag


def start():
    global work_time, work_time_sko, flag
    # work_time = int(w_time.get())
    # work_time_sko = int(w_time_sko.get())

    print('ЗАПУСК')

    working_hours()

    work_time_now1 = datetime.datetime.today()
    print(work_time_now1.strftime("%Y-%m-%d-%H.%M.%S"))  # 2017-04-05-00.18.00
    print(work_time_now1.strftime("%H.%M.%S"))  # 2017-04-05-00.18.00

    if flag == 1:
        print('Начинаем торги')
        first_data(work_time, work_time_sko)

        while input('Бот закончил свою работу\nЖелаете продолжить?\n'
                    'Если да, то нажмите y, если нет, то любую клавишу ') == "y":
            print('Запускаем прогу заново')
            return start()
    else:
        print('Ждем основных торгов')
        time.sleep(120)
        return start()

    # while input('Бот закончил свою работу\nЖелаете продолжить?\n'
    # 'Если да, то нажмите y, если нет, то любую клавишу ') == "y":


print('Введите время работы алгоритма')
work_time = int(input())
print(work_time)

print('Введите время сбора статистики')
work_time_sko = int(input())
print(work_time_sko)

start()

# window = Tk()
# window.title("Bot")
# window.geometry('1280x720')

# main_menu = Menu(window)
# window.config(menu=main_menu)

# lbl_config = Label(window, text="Установи конфиг", font=("Arial Bold", 18))
# lbl_config.place(x=20, y=10)

# lbl_w_time = Label(window, text="Время работы", font=("Arial Bold", 8))
# lbl_w_time.place(x=30, y=40)
# w_time = Entry(window)
# w_time.place(x=30, y=60)

# lbl_w_time_sko = Label(window, text="Время сбора СКО", font=("Arial Bold", 8))
# lbl_w_time_sko.place(x=30, y=100)
# w_time_sko = Entry(window)
# w_time_sko.place(x=30, y=120)

# start = Button(window, text="Рот этого казино", command=start)
# start.place(x=250, y=100)

# window.mainloop()
