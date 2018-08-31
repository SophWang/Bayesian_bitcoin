import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
rc('mathtext', default='regular')


class Evaluation(object):
    def __init__(self, prices, n, dps, step, threshold,
                 long_term_invest, initial_balance, borrowing_capacity,period):
        """
        prices: 价格数据
        n: 窗口长度, an integer
        dps: 平均价格变化
        step: 交易时间间隔
        thresohld: 进行交易的价格界限
        benchmark_returns: 市场平均回报率
        """
        self.prices = prices
        self.n = n
        self.dps = dps
        self.step = step
        self.threshold = threshold
        self.long_term_invest = long_term_invest
        self.initial_balance = initial_balance
        self.borrowing_capacity = borrowing_capacity
        self.period = period
    """
    建立虚拟账户并根据交易策略进行买卖
    返回最终账户余额和总投资金额
    """

    def visual_account(self, threshold):
        if type(threshold) == float:
            position = 0
            bank_balance = self.initial_balance
            fin_profit = [0]
            times = []
            predicted_dps = []
            actual_dps = []
            current_price = self.prices[self.n]
            costs=[]
            prices = [current_price]
            cost = 0
            for i in range(self.n + self.step, len(self.prices) - 1, self.step):
                current_price = self.prices[i]
                if self.long_term_invest:
                    if self.dps[i - self.n] > threshold and bank_balance >= -self.borrowing_capacity:
                        position += 1
                        bank_balance -= current_price
                        times.append(i)
                        prices.append(current_price)
                        predicted_dps.append(np.sum(self.dps[i - self.step - self.n: i - self.n]))
                        actual_dps.append(self.prices[i] - self.prices[i - self.step])
                        cost += current_price
                        costs.append(cost)
                        fin_profit.append(bank_balance - self.initial_balance+ position * current_price)
                    if self.dps[i - self.n] < -threshold:
                        position -= 1
                        bank_balance += current_price
                        times.append(i)
                        prices.append(current_price)
                        costs.append(0)
                        predicted_dps.append(np.sum(self.dps[i - self.step - self.n:i - self.n]))
                        actual_dps.append(self.prices[i] - self.prices[i - self.step])
                        fin_profit.append(bank_balance - self.initial_balance + position * current_price)
                else:
                    if self.dps[i - self.n] > threshold and position <= 0:
                        position += 1
                        bank_balance -= current_price
                        times.append(i)
                        prices.append(current_price)
                        predicted_dps.append(np.sum(self.dps[i - self.step:i]))
                        actual_dps.append(self.prices[i] - self.prices[i - self.step])
                        cost += current_price
                        costs.append(cost)
                        fin_profit.append(bank_balance - self.initial_balance + current_price*position)
                    if self.dps[i - self.n] < -threshold and position >= 0:
                        position -= 1
                        bank_balance += current_price
                        times.append(i)
                        prices.append(current_price)
                        costs.append()
                        predicted_dps.append(np.sum(self.dps[i - self.step:i]))
                        actual_dps.append(self.prices[i] - self.prices[i - self.step])
                        fin_profit.append(bank_balance - self.initial_balance +current_price*position)
            if position > 0:
                bank_balance += position * current_price
                times.append(len(self.prices))
            if position < 0:
                bank_balance += position * current_price
                cost -= position * current_price
                times.append(len(self.prices))
            returns=[]
            for i in range(0,len(fin_profit)):
                returns.append(fin_profit[i]/self.initial_balance)
            profit=bank_balance-self.initial_balance
            return_rate = profit / self.initial_balance
            return bank_balance, return_rate, fin_profit, prices, times, profit, cost, predicted_dps, actual_dps, costs, returns
        else:
            total_profit = []
            holding_time = []
            sample_size = []
            fin_profit = []
            for i in range(len(threshold[0])):
                bank_balance = 2000
                position = 0
                investment = 0
                step_i = self.step
                trade_times = 0
                final_profit=0
                for j in range(self.n, len(self.prices) - 1, step_i):
                    if self.dps[j - self.n] > threshold[0, i] and position <= 0:
                        position += 1
                        bank_balance -= self.prices[j]
                        final_profit = bank_balance - self.initial_balance
                        investment += self.prices[j]
                        trade_times += 1
                    if self.dps[j - self.n] < -threshold[0, i] and position >= 0:
                        position -= 1
                        bank_balance += self.prices[0, j]
                        final_profit = bank_balance - self.initial_balance
                        trade_times += 1
                current_price1 = self.prices[len(self.prices) - 1]
                if position == 1:
                    bank_balance += current_price1
                    final_profit = bank_balance - self.initial_balance
                    trade_times += 1
                if position == -1:
                    bank_balance -= current_price1
                    trade_times += 1
                    final_profit = bank_balance - self.initial_balance
                    investment += current_price1
                fin_profit.append(final_profit)
                total_profit.append(final_profit)
                if trade_times==0:
                    avg_holding_time=len(self.prices) - self.n
                else:
                    avg_holding_time = (len(self.prices) - self.n) / trade_times
                holding_time.append(avg_holding_time)
                sample_size.append(trade_times)
            fin_profit = np.array(fin_profit)
            sample_size = np.array(sample_size)
            avg_profit = fin_profit / sample_size
            return avg_profit, total_profit, sample_size, holding_time


    def correct_rate(self):
        '''计算价格变动方向预测的准确率评估算法'''
        correct = 0
        wrong = 0
        temp = self.visual_account(self.threshold)
        actual_change = temp[8]
        predicted_change = temp[7]
        for i in range(len(actual_change)):
            if (predicted_change[i] >= 0 and actual_change[i] >=0) or predicted_change[i] <=0 and (actual_change[i] <= 0):
                correct += 1
            else:
                wrong += 1
        correct_rate = correct / (correct + wrong)
        print('Correct rate is: ' + str(correct_rate))
        print('cost = ',temp[6])
        print('final profit: ', temp[5])
        print('Bank balance = ', temp[0])
        print('return_rate = ', temp[1])
        return correct_rate

    def plot_price_and_profit(self):
        '''绘制价格变化率和回报率随时间的变化'''
        temp = self.visual_account(self.threshold)
        bitcoin_price = temp[3]
        time = temp[4]
        time = np.array(time)
        returns=temp[10]
        returns=np.array(returns)
        price_change=[]
        for i in range(len(bitcoin_price)):
            price_change.append((bitcoin_price[i]-bitcoin_price[0])/bitcoin_price[0])
        price_change=np.array(price_change)
        plt.plot(time,price_change, '-',label='price change rate')
        plt.plot(time,returns,'-r',label='return rate')
        plt.grid(True)
        ax = plt.gca()
        ax.set_xlabel('time(minute)')
        ax.set_ylabel('ratio')
        plt.legend()
        plt.show()
        plt.close()

    def plot_threshold_profit(self):
        threshold = np.arange(0.1, 0.2, 0.001).reshape(1, -1)
        temp = self.visual_account(threshold)
        pnl = np.array(temp[0]).reshape(1, -1)
        total_pnl = np.array(temp[1]).reshape(1, -1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(threshold[0], pnl[0], '-b')
        ax.set_xlabel('threshold')
        ax.set_ylabel('pnl (blue)')
        ax2 = ax.twinx()
        ax2.plot(threshold[0], total_pnl[0], '-k')
        ax2.set_ylabel('total pnl (black)')
        plt.show()

    def plot_threshold_size(self):
        threshold = np.arange(0.1, 0.2, 0.001).reshape(1, -1)
        temp = self.visual_account(threshold)
        holding_size = np.array(temp[3]).reshape(1, -1)
        sample_size = np.array(temp[2]).reshape(1, -1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(threshold[0], holding_size[0], '-b')
        ax.set_xlabel('threshold')
        ax.set_ylabel('pnl (blue)')
        ax2 = ax.twinx()
        ax2.plot(threshold[0], sample_size[0], '-k')
        ax2.set_ylabel('total pnl (black)')
        plt.show()

    '''
    def sharpe_ratio(self):
        trade_price = self.visual_account(self.threshold)[3]
        point = self.visual_account(self.threshold)[3]
        C = (trade_price[-1] - trade_price[1]) / (point[-1] - point[1])
        sum = np.sum(trade_price)
        mean = sum / len(trade_price)
        b = 0
        for i in range(len(trade_price) - 1):
            b += (trade_price[i] - mean) ** 2
        sharpe_ratio = (sum - C) / b
        return sharpe_ratio
    '''

    def periodic_return(self):
        temp = self.visual_account(self.threshold)
        cost = temp[9]
        profit = temp[2]
        price = temp[3]
        periodic_return = []
        market_return = []
        period_len = len(cost)/self.period
        for i in range(self.period-1):
            profit_i = profit[int(period_len*(i+1))]
            #cost_i = np.sum(cost[int(period_len*i):int(period_len*(i+1))])
            #if cost_i==0:
                #periodic_return.append(0)
            #else:
                #periodic_return.append(profit_i/cost_i)
            periodic_return.append(profit_i/self.initial_balance)
            price_change = (price[int(period_len*(i+1))]-price[int(period_len*i)])/price[int(period_len*i)]
            market_return.append(price_change)
        return periodic_return, market_return



    if __name__ == '__main__':
        import pandas as pd
        from bayesian_model.train_test import Split
        test_train = Split(p)
        train_data = test_train()[0]
        test_data = test_train()[1]
        p = pd.read_csv('.//prices.csv')
        p1 = pd.read_csv('.//p1.csv')
        p2 = pd.read_csv('.//p2.csv')
        p3 = pd.read_csv('.//p3.csv')
