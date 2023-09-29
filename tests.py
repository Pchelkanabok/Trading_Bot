

'''
for i in range():
    for j in range():
        for k in range():
            my_test(i, j, k)
'''

def my_test(take_p, stop_l, const_buy):
    data = []
    with open('data/data_all_9sept_pm_0-1_2glass.txt', 'r') as f:
        for line in f:
            data.append(line.split(','))


    balance = 0
    shares_pref = 0
    shares_ob = 0
    deals_fix = 0
    quantity_profit = 0
    quantity_loss = 0
    deal_spread = 0
    balance_old = 0
    deals_buy = 0

    for i in range(len(data)):
        if len(data[i]) >= 6:
            deviation = float(data[i][5])
            sr_spread = float(data[i][7])
            spread_now = float(data[i][6])
            bid_ob = float(data[i][8])
            bid_pref = float(data[i][9])
            offer_ob = float(data[i][10])
            offer_pref = float(data[i][11])
            spread_now_ = float(data[i][3])
            '''
            if last_price_pref > last_price_ob:
                c = last_price_pref
                last_price_pref = last_price_ob
                last_price_ob = c
            '''
            if (spread_now <= sr_spread * (1 + deviation * take_p)) and shares_pref == 1:
                # если спред расширялся и мы встали в позицию
                # тейк-профит
               # print('фиксанули прибыль')
                #print("Баланс: ",)
                deal_spread = 0
                deals_fix += 1
                shares_pref -= 1
                shares_ob += 1
                balance += offer_pref
                balance -= bid_ob
                quantity_profit += 1

            elif (spread_now >= sr_spread * (1 - deviation * take_p)) and shares_ob == 1:
                # если спред сужался и мы встали в позицию
                # тейк-профит
                #print('фиксанули прибыль')
                deal_spread = 0
                deals_fix += 1
                shares_pref += 1
                shares_ob -= 1
                balance += offer_ob
                balance -= bid_pref
                quantity_profit += 1

            elif (spread_now > deal_spread * (1 + deviation * stop_l)) and shares_pref == 1:
                # если спред расширялся и мы встали в позицию
                # стоп-лосс
                #print('фиксанули убыток')
                deal_spread = 0
                deals_fix += 1
                shares_pref -= 1
                shares_ob += 1
                balance -= bid_ob
                balance += offer_pref
                quantity_loss += 1

            elif (deal_spread * (1 - deviation * stop_l) > spread_now) and shares_ob == 1:
                # если спред сужался и мы встали в позицию
                # стоп-лосс
                #print('фиксанули убыток')
                deal_spread = 0
                deals_fix += 1
                shares_pref += 1
                shares_ob -= 1
                balance += offer_ob
                balance -= bid_pref
                quantity_loss += 1

            else:
                if spread_now > sr_spread * (1 + deviation) * const_buy and shares_ob == 0 and shares_pref == 0 and spread_now_ > sr_spread:
                    # if spread_now > sr_spread + sko_real and shares_ob == 0 and shares_pref == 0:
                #    print('спред расширился, продали обыкновенные, купили префы')

                    balance_old = balance
                    deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                    deals_buy += 1
                    balance += offer_ob
                    shares_ob -= 1  # зашортили обыкновенные
                    balance -= bid_pref  # купили в лонг префы
                    shares_pref += 1

                if sr_spread * (1 - deviation) > spread_now > spread_now_ and shares_ob == 0 and shares_pref == 0 :
                    # if spread_now < sr_spread - sko_real and shares_ob == 0 and shares_pref == 0:
                 #   print('спред сузился, купили обыкновенные, продали префы')

                    balance_old = balance
                    deal_spread = spread_now  # запоминаем спред покупки, выстраиваем стоп-лоссы и тейк-профиты от него
                    deals_buy += 1
                    balance -= bid_ob
                    shares_ob += 1  # зашортили обыкновенные
                    balance += offer_pref  # купили в лонг префы
                    shares_pref -= 1

    if deals_fix + deals_buy < 1050:
        print(len(data))
        profit = balance - (deals_fix + deals_buy) * 3.72
        print('ИТОГО: ---------------------------------------')
        print('Комиссия 1:', (deals_fix + deals_buy) * 3.72)
        print('Чистая прибыль 1:', profit)
        print('Всего сделок:', deals_fix + deals_buy)
        print('----------------------------------------------')
        print('Кол-во убыточных сделок:', quantity_loss)
        print('Кол-во прибыльных сделок:', quantity_profit)
    return [deals_fix + deals_buy, balance - (deals_fix + deals_buy) * 3.72]

take_p = 0.2

#ПОМЕНЯТЬ ПУТИ К ФАЙЛАМ
stop_l = 3.5
const_buy = 1
my_test(take_p, stop_l, const_buy)

'''
for j in range(100, 500, 50):
    for i in range(0,int(j/10),1):
        #for k in range():
        m = my_test(i/10, j/100, 1)
        if m[0]<1050:
            print("Stop ", j/100)
            print("Take ", i/10)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
'''

