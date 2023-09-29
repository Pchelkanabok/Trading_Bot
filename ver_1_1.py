from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
import time
from statistics import mean
import csv
import random
import os
import math

last_price_pref, last_price_ob, sec_code_pref, sec_code_ob = 0, 0, 0, 0
best_glass_bid_pref, best_glass_offer_pref, best_glass_bid_ob, best_glass_offer_ob = 0, 0, 0, 0


def first_data(work_time_, work_time_sko_):
    work_time = work_time_
    work_time_sko = work_time_sko_
    global last_price_pref, last_price_ob, sec_code_pref, sec_code_ob
    global best_glass_bid_pref, best_glass_offer_pref, best_glass_bid_ob, best_glass_offer_ob

    qp_provider = QuikPy()
    class_code = 'SPBFUT'  # Класс тикера
    sec_code_pref = 'SPM2'  # Тикер - префы
    sec_code_ob = 'SRM2'  # Тикер - обык

    def write_in_data(var):
        # Функция записи в файл даты
        with open(file="C:/QUIK_AD/Quik/lua/data/data_all.txt", mode="a", encoding="utf-8") as f:
            if var == '\n':
                f.write(var)
            else:
                str_zap = str(var)+','
                f.write(str_zap)

    def pref_sell():
        trans_id = random.getrandbits(6)
        print('trans_id', trans_id)
        # Новая лимитная/рыночная заявка для продажи префов
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(trans_id),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00JHC',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': class_code,  # Код площадки
            'SECCODE': sec_code_pref,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая рыночная заявка отправлена на рынок:'
              f'{qp_provider.SendTransaction(transaction)["data"]}')

    def pref_buy():
        trans_id = random.getrandbits(6)
        # Новая лимитная/рыночная заявка для покупки префов
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(trans_id),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00JHC',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': class_code,  # Код площадки
            'SECCODE': sec_code_pref,  # Код тикера
            'OPERATION': 'B',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая рыночная заявка отправлена на рынок:'
              f'{qp_provider.SendTransaction(transaction)["data"]}')

    def ob_sell():
        trans_id = random.getrandbits(6)
        # Новая лимитная/рыночная заявка для продажи обыкновенных
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(trans_id),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00JHC',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': class_code,  # Код площадки
            'SECCODE': sec_code_ob,  # Код тикера
            'OPERATION': 'S',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая рыночная заявка отправлена на рынок:'
              f'{qp_provider.SendTransaction(transaction)["data"]}')

    def ob_buy():
        trans_id = random.getrandbits(6)
        # Новая лимитная/рыночная заявка для покупки обыкновенных
        # Все значения должны передаваться в виде строк
        transaction = {
            'TRANS_ID': str(trans_id),  # Номер транзакции задается клиентом
            'CLIENT_CODE': '',  # Код клиента. Для фьючерсов его нет
            'ACCOUNT': 'SPBFUT00JHC ',  # Счет
            'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
            'CLASSCODE': class_code,  # Код площадки
            'SECCODE': sec_code_ob,  # Код тикера
            'OPERATION': 'B',  # B = покупка, S = продажа
            'PRICE': '0',  # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена
            # в зависимости от направления. Для остальных рыночных заявок цена = 0
            'QUANTITY': str(1),  # Кол-во в лотах
            'TYPE': 'M'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка
        print(f'Новая рыночная заявка отправлена на рынок:'
              f'{qp_provider.SendTransaction(transaction)["data"]}')

    def true_time(x_, start_time_):
        time_now = time.time()
        return x_, round(time_now - start_time_, 2)

    def price():
        global last_price_pref, last_price_ob, sec_code_pref, sec_code_ob
        last_price_pref = float(qp_provider.GetParamEx(class_code, sec_code_pref, 'LAST')['data']['param_value'])
        last_price_ob = float(qp_provider.GetParamEx(class_code, sec_code_ob, 'LAST')['data']['param_value'])

        if last_price_pref == last_price_ob:
            time.sleep(120)
            price()

        return last_price_pref, last_price_ob

    def stock_glass():
        global last_price_pref, last_price_ob, sec_code_pref, sec_code_ob
        global best_glass_bid_pref, best_glass_offer_pref, best_glass_bid_ob, best_glass_offer_ob

        price()

        best_glass_bid_pref = qp_provider.GetQuoteLevel2(class_code, sec_code_pref)['data']['bid'][-1]['price']
        print(sec_code_pref, ' bid, best ', best_glass_bid_pref)

        best_glass_offer_pref = qp_provider.GetQuoteLevel2(class_code, sec_code_pref)['data']['offer'][0]['price']
        print(sec_code_pref, ' offer, best ', best_glass_offer_pref)

        best_glass_bid_ob = qp_provider.GetQuoteLevel2(class_code, sec_code_ob)['data']['bid'][-1]['price']
        print(sec_code_ob, ' bid, best ', best_glass_bid_ob)

        best_glass_offer_ob = qp_provider.GetQuoteLevel2(class_code, sec_code_ob)['data']['offer'][0]['price']
        print(sec_code_ob, ' offer, best ', best_glass_offer_ob)

        return best_glass_bid_pref, best_glass_offer_pref, best_glass_bid_ob, best_glass_offer_ob
        # offer - продажа, bid - покупка

    def test(work_time_, work_time_sko_):
        # 1-ый параметр - время работы программы для торгов,
        # 2-ой-время которое программа собирает данные перед начало торгов
        balance, deals_fix, deals_buy, deal_spread, quantity_loss, quantity_profit \
            = 0, 0, 0, 0, 0, 0
        shares_pref = int(qp_provider.GetFuturesHoldings()['data'][0]['totalnet'])
        shares_ob = int(qp_provider.GetFuturesHoldings()['data'][1]['totalnet'])
        nakop, spread_now_mas, val_deal_mas_open, val_deal_mas_close, spread_deal_mas, time_deal_mas_open, \
            time_deal_mas_close, balance_change, coast_pref, coast_ob, sko_mas, sr_spread_mas, kv_nakop_for_real_sko,\
            all_balance = [], [], [], [], [], [], [], [], [], [], [], [], [], []

        global last_price_pref, last_price_ob, sec_code_pref, sec_code_ob

        start_time = time.time()

        for x in range(work_time_sko_ * 10):
            print('INFO', ' out of ', work_time_sko_ * 10, ' cycles passed ', x)
            # Последние цены сделок:
            price()
            spread_now_mas.append(abs(last_price_ob - last_price_pref))
            sr_spread = mean(spread_now_mas)
            spread_now = abs(last_price_ob - last_price_pref)
            nakop.append((abs(spread_now - sr_spread) / sr_spread))
            kv_nakop_for_real_sko.append(abs(spread_now - sr_spread) ** 2)
            time.sleep(0.1)

        deviation = mean(nakop)
        sko_real = math.sqrt(mean(kv_nakop_for_real_sko))

        print('Average accumulated spread:', sr_spread)
        print('Deviation %: ', deviation * 100)
        print('Real SKO:', sko_real)

        xx = 0
        while xx <= work_time_ or shares_pref != 0 or shares_ob != 0:
            for j in range(10):
                price()
                spread_now = abs(last_price_ob - last_price_pref)
                spread_now_mas.pop(0)
                spread_now_mas.append(spread_now)
                sr_spread = mean(spread_now_mas)
                nakop.pop(0)
                nakop.append((abs(spread_now - sr_spread) / sr_spread))
                time.sleep(0.1)

            price()
            shares_pref = int(qp_provider.GetFuturesHoldings()['data'][0]['totalnet'])
            shares_ob = int(qp_provider.GetFuturesHoldings()['data'][1]['totalnet'])

            spread_now = abs(last_price_ob - last_price_pref)
            deviation = mean(nakop)
            print('Deviation %: ', deviation * 100)

            if shares_pref == 0 and shares_ob == 0:
                if (spread_now <= sr_spread * (1 + deviation * 0.1)) and shares_pref == 1 and shares_ob == -1:
                    # если спред расширялся и мы встали в позицию
                    # тейк-профит
                    print('PROFIT')
                    stock_glass()
                    deal_spread = 0
                    deals_fix += 1
                    balance += int(best_glass_offer_pref)
                    balance -= int(best_glass_bid_ob)
                    quantity_profit += 1

                    pref_sell()
                    ob_buy()

                elif (spread_now >= sr_spread * (1 - deviation * 0.1)) and shares_ob == 1 and shares_pref == -1:
                    # если спред сужался и мы встали в позицию
                    # тейк-профит
                    print('PROFIT')
                    stock_glass()
                    deal_spread = 0
                    deals_fix += 1
                    balance += int(best_glass_offer_ob)
                    balance -= int(best_glass_bid_pref)
                    quantity_profit += 1

                    pref_buy()
                    ob_sell()

                elif (spread_now > deal_spread * (1 + deviation * 3.5)) and shares_pref == 1 and shares_ob == -1:
                    # если спред расширялся и мы встали в позицию
                    # стоп-лосс
                    print('LOSS')
                    stock_glass()
                    deal_spread = 0
                    deals_fix += 1
                    balance -= int(best_glass_bid_ob)
                    balance += int(best_glass_offer_pref)
                    quantity_loss += 1

                    pref_sell()
                    ob_buy()

                elif (deal_spread * (1 - deviation * 3.5) > spread_now) and shares_ob == 1 and shares_pref == -1:
                    # если спред сужался и мы встали в позицию
                    # стоп-лосс
                    print('LOSS')
                    stock_glass()
                    deal_spread = 0
                    deals_fix += 1
                    balance += int(best_glass_offer_ob)
                    balance -= int(best_glass_bid_pref)
                    quantity_loss += 1

                    pref_buy()
                    ob_sell()

                else:
                    if spread_now > sr_spread * (1 + deviation) and shares_ob == 0 and shares_pref == 0:
                        print('Expansion, sell ob, buy pref')

                        stock_glass()

                        balance_old = balance
                        deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                        deals_buy += 1
                        balance += int(best_glass_offer_ob)
                        balance -= int(best_glass_bid_pref)

                        pref_buy()
                        ob_sell()

                    elif spread_now < sr_spread * (1 - deviation) and shares_ob == 0 and shares_pref == 0:
                        print('Narrowing, buy ob, sell pref')

                        stock_glass()

                        balance_old = balance
                        deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                        deals_buy += 1
                        balance += int(best_glass_offer_pref)
                        balance -= int(best_glass_bid_ob)

                        pref_sell()
                        ob_buy()

            xx += 1

            all_balance.append(balance)
            print('MONEY: ', balance, '  out of ', work_time, 'cycles passed, time spent:',
                  true_time(xx, start_time))

            write_in_data(time.time())
            write_in_data(float(qp_provider.GetParamEx(class_code, 'SRM2', 'LAST')['data']['param_value']))
            write_in_data(float(qp_provider.GetParamEx(class_code, 'SPM2', 'LAST')['data']['param_value']))
            write_in_data(abs(float(qp_provider.GetParamEx(class_code, 'SRM2', 'LAST')['data']['param_value'])
                              - float(qp_provider.GetParamEx(class_code, 'SPM2', 'LAST')['data']['param_value'])))
            write_in_data(deviation)
            write_in_data(sr_spread)
            write_in_data(best_glass_bid_ob)
            write_in_data(best_glass_bid_pref)
            write_in_data(best_glass_offer_ob)
            write_in_data(best_glass_offer_pref)
            write_in_data('\n')

        profit = balance - (deals_fix + deals_buy) * 3.72
        print('RESULT: ---------------------------------------')
        print('Commission:', (deals_fix + deals_buy) * 3.72)
        print('Net profit:', profit)
        print('Total deals:', deals_fix + deals_buy)
        print('Profit/loss:', quantity_profit, '/', quantity_loss)
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

        qp_provider.CloseConnectionAndThread()

    test(work_time, work_time_sko)

