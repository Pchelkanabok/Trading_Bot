from test_1 import first_data

from tkinter import Tk, Button, Menu, Entry
from tkinter.ttk import Label


def read_mas_in_file(name):     # Функция чтения массива из файла
    b = []
    f = open("C:/QUIK_AD/Quik/lua/data/" + name + ".txt", "w+")
    # open(file="C:/QUIK_VTB/lua/data/1.txt", mode="r+", encoding="utf-8")
    for line in f:
        b.append(*[int(x) for x in line.split()])
    f.close()
    return b


def start():
    work_time = int(w_time.get())
    work_time_sko = int(w_time_sko.get())
    take_profit = float(t_profit.get())
    stop_loss = float(s_loss.get())
    #call = call_.get()

    for i in range(5):
        # 5 оборотов цикла ровно на час
        first_data(work_time, work_time_sko, take_profit, stop_loss)   # Сейчас 2 минуты сбора инфы, потом 10 минут торгов соответственно

        # Далее тут буду делать чтения циферок из фала и построения графиков каждую итерацию цикла
        # (ну в данном случае каждые 10 мин)

        # мб сделаю общую базу данных в экселе тут, ну крч работа с массивами собранными за какое-то время
        # будет производиться тут


window = Tk()
window.title("Bot")
window.geometry('1280x720')

mainmenu = Menu(window)
window.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
#filemenu.add_command(label="Редактировать...", command=edit)
#mainmenu.add_cascade(label="Меню", menu=filemenu)

lbl_config = Label(window, text="Установи конфиг", font=("Arial Bold", 18))
lbl_config.place(x=20, y=10)

lbl_w_time = Label(window, text="Время работы", font=("Arial Bold", 8))
lbl_w_time.place(x=30, y=40)
w_time = Entry(window)
w_time.place(x=30, y=60)

lbl_w_time_sko = Label(window, text="Время сбора СКО", font=("Arial Bold", 8))
lbl_w_time_sko.place(x=30, y=100)
w_time_sko = Entry(window)
w_time_sko.place(x=30, y=120)

lbl_t_profit = Label(window, text="Профит, в %", font=("Arial Bold", 8))
lbl_t_profit.place(x=30, y=160)
t_profit = Entry(window)
t_profit.place(x=30, y=180)

lbl_s_loss = Label(window, text="Стоп, в %", font=("Arial Bold", 8))
lbl_s_loss.place(x=30, y=220)
s_loss = Entry(window)
s_loss.place(x=30, y=240)

#call_ = Entry(window)
#call_.place(x=30, y=150)

start = Button(window, text="Рот этого казино", command=start)
start.place(x=250, y=100)


window.mainloop()


