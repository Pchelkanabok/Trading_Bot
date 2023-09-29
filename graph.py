import matplotlib.pyplot as plt
import matplotlib.animation as animation
from clear_data import clear_d

#clear_d()

plt.style.use('dark_background')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    data = []
    func_spread, func_sr_spread, func_sko_down, func_sko_up = [], [], [], []

    with open('data/data_all.txt', 'r') as f:
        for line in f:
            data.append(line.split(','))
    # print(data)

    for i in range(len(data)):
        if i > 0:
            if len(data[i]) >= 6:
                func_spread.append(float(data[i][3]))
                func_sr_spread.append(float(data[i][5]))
                func_sko_down.append(float(data[i][5]) * (1 - float(data[i][4])))
                func_sko_up.append(float(data[i][5]) * (1 + float(data[i][4])))

    ax1.clear()
    ax1.plot(func_spread)
    ax1.plot(func_sr_spread)
    ax1.plot(func_sko_down)
    ax1.plot(func_sko_up)
    # ax1.plot(balance)
    plt.xlabel('Время')
    plt.ylabel('Цена')
    plt.title('Илья, называй переменные нормально')
    # ax1.set_xlim([0, 100])
    # ax1.set_ylim([0,300])

ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()
