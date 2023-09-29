from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
import time
from statistics import mean
from statistics import stdev
import csv


def first_data(work_time_, work_time_sko_, take_profit_, stop_loss_):
    def write_mas_in_file(mas, name):
        # Функция записи в файл
        with open(file="C:/QUIK_AD/Quik/lua/data/" + name + ".txt", mode="w+", encoding="utf-8") as f:
            for listitem in mas:
                f.write('%s\n' % listitem)

    work_time = work_time_
    work_time_sko = work_time_sko_
    take_profit = take_profit_
    stop_loss = stop_loss_

    config_mas = ['work_time', work_time, 'work_time_sko', work_time_sko,
                  'take_profit', take_profit, 'stop_loss', stop_loss]

    write_mas_in_file(config_mas, "Config")

    # Точка входа при запуске этого скрипта
    qpProvider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
    # qpProvider = QuikPy(Host='<Ваш IP адрес>')  # Вызываем конструктор QuikPy с подключением
    # к удаленному компьютеру с QUIK

    # firmId = 'MC0005500000'  # Фирма
    classCode = 'SPBFUT'  # Класс тикера
    # classCode = 'SPBFUT'  # Класс тикера
    secCode_pref = 'SPM2'  # Тикер - префы
    secCode_ob = 'SRM2'  # Тикер - обык

    # firmId = 'SPBFUT'  # Фирма
    # classCode = 'SPBFUT'  # Класс тикера
    # secCode = 'SiH2'  # Для фьючерсов: <Код тикера><Месяц экспирации: 3-H, 6-M, 9-U, 12-Z><Последняя цифра года>

    # Данные тикера
    securityInfo = qpProvider.GetSecurityInfo(classCode, secCode_pref)["data"]
    # print(securityInfo)
    print(f'Информация о тикере {classCode}.{secCode_pref} ({securityInfo["short_name"]}):')
    print('Валюта:', securityInfo['face_unit'])
    print('Кол-во десятичных знаков:', securityInfo['scale'])
    print('Лот:', securityInfo['lot_size'])
    print('Шаг цены:', securityInfo['min_price_step'])

    # Торговый счет тикера
    tradeAccount = qpProvider.GetTradeAccount(classCode)["data"]  # Торговый счет для класса тикера
    print(f'Торговый счет для тикера класса {classCode}: {tradeAccount}')

    # Последняя цена сделки
    lastPrice_pref = float(
        qpProvider.GetParamEx(classCode, secCode_pref, 'LAST')['data']['param_value'])  # Последняя цена сделки
    lastPrice_ob = float(
        qpProvider.GetParamEx(classCode, secCode_ob, 'LAST')['data']['param_value'])  # Последняя цена сделки

    TransId = 0

    def csv_file_writer(work_time, work_time_sko, take_profit, stop_loss, profit):
        with open("C:/QUIK_AD/Quik/lua/data/results.csv", mode="a", newline='', encoding='utf-16') as f:
            file_writer = csv.writer(f, delimiter=" ", quoting=csv.QUOTE_MINIMAL)
            buffer = ['Время работы:', work_time, 'Время сбора статы:', work_time_sko,
                      'Тейк:', take_profit, 'Стоп:', stop_loss, 'Профит:', profit]
            file_writer.writerow(buffer)
            buffer.clear()

    def pref_sell():
        TransId =+ 1
        # Новая лимитная/рыночная заявка для продажи префов
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00PST',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode_pref,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая лимитная/рыночная заявка отправлена на рынок:'
              f'{qpProvider.SendTransaction(transaction)["data"]}')

    def pref_buy():
        TransId =+ 1
        # Новая лимитная/рыночная заявка для покупки префов
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00PST',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode_pref,  # Код тикера
            'OPERATION': 'B',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая лимитная/рыночная заявка отправлена на рынок:'
              f'{qpProvider.SendTransaction(transaction)["data"]}')

    def ob_sell():
        TransId = + 1
        # Новая лимитная/рыночная заявка для продажи обыкновенных
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00PST',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode_ob,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая лимитная/рыночная заявка отправлена на рынок:'
              f'{qpProvider.SendTransaction(transaction)["data"]}')

    def ob_buy():
        TransId = + 1
        # Новая лимитная/рыночная заявка для покупки обыкновенных
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(TransId),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00PST',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': classCode,  # Код площадки
            'SECCODE': secCode_ob,  # Код тикера
            'OPERATION': 'B',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая лимитная/рыночная заявка отправлена на рынок:'
              f'{qpProvider.SendTransaction(transaction)["data"]}')

    def check_top_share():
        if lastPrice_pref > lastPrice_ob:
            # меняем тикеры местами, тем самым переворачиваем стратегию
            secCode_pref = 'SRM2'  # Тикер для обыкновенных, но используем для префов
            secCode_ob = 'SPM2'  # Тикер - наоборот
        elif lastPrice_pref < lastPrice_ob:
            secCode_pref = 'SPM2'  # Тикер для префов
            secCode_ob = 'SRM2'
        else:
            pass

    def true_time(start_time_):
        time_now = time.time()
        return (work_time - time_now + start_time_) // 0.01 * 0.01

    def test(work_time_, work_time_sko_, take_profit_, stop_loss_):
        # 1-ый параметр - время работы программы для торгов,
        # 2-ой-время которое программа собирает данные перед начало торгов
        val = 0
        shares_pref = 0
        shares_ob = 0
        deals_fix = 0
        deals_buy = 0
        deal_spread = 0

        nakop = []
        spread_now_mas = []

        val_deal_mas_open = []
        val_deal_mas_close = []
        spread_deal_mas = []
        time_deal_mas_open = []
        time_deal_mas_close = []
        balance_change = []
        coast_pref = []
        coast_ob = []
        quantity_loss = 0
        quantity_profit = 0
        work_time_sko = work_time_sko_ * 10
        # сначала необходимо собирать инфу о спреде 2 минуты, чтобы посчитать средний и только потом начинать торговать

        start_time = time.time()


        #def sko_calc():

        for i in range(work_time_sko):
            check_top_share()
            # Последние цены сделок:
            lastPrice_pref = float(
                qpProvider.GetParamEx(classCode, secCode_pref, 'LAST')['data']['param_value'])
            lastPrice_ob = float(
                qpProvider.GetParamEx(classCode, secCode_ob, 'LAST')['data']['param_value'])
            spread_now_mas.append(abs(lastPrice_ob - lastPrice_pref))
            sr_spread = mean(spread_now_mas)
            spread_now = abs(lastPrice_ob - lastPrice_pref)
            nakop.append((abs(spread_now - sr_spread) / (sr_spread)))
            time.sleep(0.1)

        sko = sum(nakop) / work_time_sko
        print(len(nakop))
        print(nakop)

        print('Cтандартное отклонение: ', stdev(spread_now_mas))
        print('СКО в %: ', sko * 100)
        print('Средний накопленный спред:', sr_spread)
        # processing_time = time.clock()

        n = work_time_

        for i in range(n):
            check_top_share()
            for j in range(10):
                lastPrice_pref = float(
                    qpProvider.GetParamEx(classCode, secCode_pref, 'LAST')['data'][
                        'param_value'])  # Последняя цена сделки
                lastPrice_ob = float(
                    qpProvider.GetParamEx(classCode, secCode_ob, 'LAST')['data'][
                        'param_value'])  # Последняя цена сделки

                coast_pref.append(lastPrice_pref)
                coast_ob.append(lastPrice_ob)
                spread_now = abs(lastPrice_ob - lastPrice_pref)
                spread_now_mas.pop(0)
                spread_now_mas.append(spread_now)
                sr_spread = mean(spread_now_mas)
                nakop.pop(0)
                nakop.append((abs(spread_now - sr_spread) / (sr_spread)))

                time.sleep(0.1)

            lastPrice_pref = float(
                qpProvider.GetParamEx(classCode, secCode_pref, 'LAST')['data']['param_value'])  # Последняя цена сделки
            lastPrice_ob = float(
                qpProvider.GetParamEx(classCode, secCode_ob, 'LAST')['data']['param_value'])  # Последняя цена сделки

            spread_now = abs(lastPrice_ob - lastPrice_pref)

            sko = sum(nakop) / work_time_sko
            # print('sko в %:', sko*100)

            if (spread_now <= deal_spread * (1-take_profit*0.01)) and shares_pref == 1:
                # если спред расширялся и мы встали в позицию
                # тейк-профит
                print('фиксанули прибыль')
                deal_spread = 0
                deals_fix = deals_fix + 1
                shares_pref = shares_pref - 1
                shares_ob = shares_ob + 1
                val = val + lastPrice_pref
                val = val - lastPrice_ob
                # print('префы', shares_pref)
                # print('обык', shares_ob)

                quantity_profit = quantity_profit + 1
                time_deal_mas_close.append(time.time())
                val_deal_mas_close.append(val)
                spread_deal_mas.append(spread_now)
                balance_change.append(val - val1)

                #pref_sell()
                #ob_buy()

            elif (spread_now >= deal_spread * (1+take_profit*0.01)) and shares_ob == 1:
                # если спред сужался и мы встали в позицию
                # тейк-профит
                print('фиксанули прибыль')
                deal_spread = 0
                deals_fix = deals_fix + 1
                shares_pref = shares_pref + 1
                shares_ob = shares_ob - 1
                val = val + lastPrice_ob
                val = val - lastPrice_pref
                # print('префы', shares_pref)
                # print('обык', shares_ob)

                quantity_profit = quantity_profit + 1
                time_deal_mas_close.append(time.time())
                val_deal_mas_close.append(val)
                spread_deal_mas.append(spread_now)
                balance_change.append(val - val1)

                #pref_buy()
                #ob_sell()

            elif (spread_now > deal_spread * (1+stop_loss*0.01)) and shares_pref == 1:
                # если спред расширялся и мы встали в позицию
                # стоп-лосс
                print('фиксанули убыток')
                deal_spread = 0
                deals_fix = deals_fix + 1
                shares_pref = shares_pref - 1
                shares_ob = shares_ob + 1
                val = val - lastPrice_ob
                val = val + lastPrice_pref
                # print('префы', shares_pref)
                # print('обык', shares_ob)

                quantity_loss = quantity_loss + 1
                time_deal_mas_close.append(time.time())
                val_deal_mas_close.append(val)
                spread_deal_mas.append(spread_now)
                balance_change.append(val - val1)

                #pref_sell()
                #ob_buy()

            elif (deal_spread * (1-stop_loss*0.01) > spread_now) and shares_ob == 1:
                # если спред сужался и мы встали в позицию
                # стоп-лосс
                print('фиксанули убыток')
                deal_spread = 0
                deals_fix = deals_fix + 1
                shares_pref = shares_pref + 1
                shares_ob = shares_ob - 1
                val = val + lastPrice_ob
                val = val - lastPrice_pref
                # print('префы', shares_pref)
                # print('обык', shares_ob)

                quantity_loss = quantity_loss + 1
                time_deal_mas_close.append(time.time())
                val_deal_mas_close.append(val)
                spread_deal_mas.append(spread_now)
                balance_change.append(val - val1)

                #pref_buy()
                #ob_sell()

            else:
                if spread_now > sr_spread * (1 + sko) and shares_ob == 0 and shares_pref == 0:
                    print('спред расширился, продали обыкновенные, купили префы')

                    val1 = val

                    deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                    deals_buy = deals_buy + 1
                    val = val + lastPrice_ob
                    shares_ob = shares_ob - 1  # зашортили обыкновенные
                    val = val - lastPrice_pref  # купили в лонг префы
                    shares_pref = shares_pref + 1

                    time_deal_mas_open.append(time.time())
                    val_deal_mas_open.append(val1)
                    spread_deal_mas.append(deal_spread)

                    # Новая лимитная/рыночная заявка для покупки префов
                    # Все значения должны передаваться в виде строк
                    #pref_buy()

                    # Новая лимитная/рыночная заявка для продажи обыкновенных
                    # Все значения должны передаваться в виде строк
                    #ob_sell()

                    # print('if1')
                    # print('БАЛАНС: ------------------------------------------')
                    # print('префы', shares_pref)
                    # print('обык', shares_ob)
                    # print('--------------------------------------------------')

                if spread_now < sr_spread * (1 - sko) and shares_ob == 0 and shares_pref == 0:
                    print('спред сузился, купили обыкновенные, продали префы')

                    val1 = val

                    deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                    deals_buy = deals_buy + 1
                    val = val - lastPrice_ob
                    shares_ob = shares_ob + 1  # зашортили обыкновенные
                    val = val + lastPrice_pref  # купили в лонг префы
                    shares_pref = shares_pref - 1

                    time_deal_mas_open.append(time.time())
                    val_deal_mas_open.append(val1)
                    spread_deal_mas.append(deal_spread)

                    # Новая лимитная/рыночная заявка для продажи префов
                    # Все значения должны передаваться в виде строк
                    #pref_sell()

                    # Новая лимитная/рыночная заявка для покупки обыкновенных
                    # Все значения должны передаваться в виде строк
                    #ob_buy()



                    # print('if2')
                    # print('БАЛАНС: ------------------------------------------')
                    # print('префы', shares_pref)
                    # print('обык', shares_ob)
                    # print('--------------------------------------------------')

            print('деньги: ', val, 'времени осталось:', true_time(start_time))
            # print('спред сейчас: ', spread_now)
            # print('средний спред: ', sr_spread)
            # time.sleep(5)

        # list_avg = mean(spread_now_mas)
        # print('Средний спред:', list_avg)

        profit = val - (deals_fix + deals_buy) * 3.72

        print('ИТОГО: ---------------------------------------')
        # print('Оборот:', cash_turnover)
        # print('Комиссия:', commission_vtb + commission_market)
        print('Комиссия 1:', (deals_fix + deals_buy) * 3.72)
        # print('Чистая прибыль:', val - commission_vtb - commission_market - 1000000)
        print('Чистая прибыль 1:', profit)
        print('Всего сделок:', deals_fix + deals_buy)
        # print('Время торговли: ', processing_time)
        print('----------------------------------------------')

        print('МАССИВЫ ДАННЫХ: ---------------------------------------')
        print('Баланс на момент открытия сделки:', val_deal_mas_open)
        print('Баланс на момент закрытия сделки:', val_deal_mas_close)
        print('История изменения баланса:', balance_change)
        print('Спред каждой сделки', spread_deal_mas)
        print('Время открытия каждой сделки:', time_deal_mas_open)
        print('Время закрытия каждой сделки:', time_deal_mas_close)
        print('Кол-во убыточных сделок:', quantity_loss)
        print('Кол-во прибыльных сделок:', quantity_profit)

        # Реализация сохранения данных в разные файлы (Для каждого массива свой файл)

        # with open(file="C:/QUIK_VTB/lua/data/1.txt", mode="r+", encoding="utf-8") as f:
        # for listitem in val_deal_mas_open:
        # f.write('%s\n' % listitem)

        # write_mas_in_file(val_deal_mas_open)
        write_mas_in_file(val_deal_mas_open, "Balance_open")
        write_mas_in_file(val_deal_mas_close, "Balance_close")
        write_mas_in_file(balance_change, "History_balance")
        write_mas_in_file(spread_deal_mas, "Spreads")
        write_mas_in_file(time_deal_mas_open, "Time_open")
        write_mas_in_file(time_deal_mas_close, "Time_close")
        write_mas_in_file(coast_pref, "Coast_pref")
        write_mas_in_file(coast_ob, "Coast_ob")

        csv_file_writer(work_time, work_time_sko, take_profit, stop_loss, profit)

        # Выход
        qpProvider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляра

        input()

    test(work_time, work_time_sko, take_profit, stop_loss)
