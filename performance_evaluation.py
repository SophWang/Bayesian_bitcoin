import matplotlib.pyplot as plt
import numpy as np
from empyrical import max_drawdown, alpha_beta
from matplotlib import rc
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
rc('mathtext', default='regular')


class Evaluation(object):
    def __init__(self, prices, n, dps, step, threshold,
                 benchmark_returns, len_of_benchmark, holding_time, sample_size, long_term_invest):
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
        self.benchmark_returns = benchmark_returns
        self.len_of_benchmark = len_of_benchmark
        self.holding_time = holding_time
        self.sample_size = sample_size
        self.long_term_invest = long_term_invest

    """
    建立虚拟账户并根据交易策略进行买卖
    返回最终账户余额和总投资金额
    """

    def visual_account(self, threshold):
        if type(threshold) == float:
            bank_balance = 2000
            position = 0
            investment = 0
            step_i = self.step
            profit = []
            price = []
            times = []
            hist_balance = np.random.randn(self.len_of_benchmark, 1)
            hist_cost = np.random.randn(self.len_of_benchmark, 1)
            for i in range(self.n, len(self.prices[0]) - 1, step_i):
                current_price = self.prices[0, i]
                if i <= (self.n + self.len_of_benchmark - 1):
                    hist_cost[i - self.n, 0] = self.prices[0, i]
                if self.long_term_invest == True:
                    if self.dps[i - self.n] > threshold:
                        position += 1
                        bank_balance -= self.prices[0, i]
                        profit.append(bank_balance - 2000 + position * current_price)
                        price.append(self.prices[0, i])
                        times.append(i)
                        investment += self.prices[0, i]
                    if self.dps[i - self.n] < -threshold:
                        position -= 1
                        bank_balance += self.prices[0, i]
                        profit.append(bank_balance - 2000 + position * current_price)
                        price.append(self.prices[0, i])
                        times.append(i)
                else:
                    if self.dps[i - self.n] > threshold and position <= 0:
                        position += 1
                        bank_balance -= self.prices[0, i]
                        profit.append(bank_balance - 2000 + position * current_price)
                        price.append(self.prices[0, i])
                        times.append(i)
                        investment += self.prices[0, i]
                    if self.dps[i - self.n] < -threshold and position >= 0:
                        position -= 1
                        bank_balance += self.prices[0, i]
                        profit.append(bank_balance - 2000 + position * current_price)
                        price.append(self.prices[0, i])
                        times.append(i)
                if i <= (self.n + self.len_of_benchmark - 1):
                    hist_balance[i - self.n, 0] = bank_balance
            current_price1 = self.prices[0, len(self.prices[0]) - 1]
            if position == 1:
                bank_balance += current_price1
            if position == -1:
                bank_balance -= current_price1
                investment += current_price1
            final_profit = np.random.randn(1, len(profit))
            final_profit[0] = profit[0]
            for k in range(1, len(profit)):
                final_profit[0, k] = final_profit[0, k - 1] + profit[k] - profit[k - 1]
            return bank_balance, hist_balance, hist_cost, final_profit, price, times, profit, investment
        else:
            total_profit = []
            avg_profit = []
            for i in range(len(threshold[0])):
                bank_balance = 2000
                position = 0
                investment = 0
                step_i = self.step
                profit = []
                for j in range(self.n, len(self.prices[0]) - 1, step_i):
                    current_price = self.prices[0, j]
                    if self.dps[j - self.n] > threshold[0, i] and position <= 0:
                        position += 1
                        bank_balance -= self.prices[0, j]
                        profit.append(bank_balance - 2000 + position * current_price)
                        investment += self.prices[0, j]
                    if self.dps[j - self.n] < -threshold[0, i] and position >= 0:
                        position -= 1
                        bank_balance += self.prices[0, j]
                        profit.append(bank_balance - 2000 + position * current_price)
                current_price1 = self.prices[0, len(self.prices[0]) - 1]
                if position == 1:
                    bank_balance += current_price1
                if position == -1:
                    bank_balance -= current_price1
                    investment += current_price1
                final_profit = np.random.randn(1, len(profit))
                final_profit[0] = profit[0]
                profit_sum = 0
                for k in range(1, len(profit)):
                    final_profit[0, k] = final_profit[0, k - 1] + profit[k] - profit[k - 1]
                    profit_sum += profit[k]
                avg = profit_sum / len(profit)
                avg_profit.append(avg)
                total_profit.append(profit_sum)
            return avg_profit, total_profit
    """
    计算最大回撤率
    返回最大回撤率，实际收益和按照Beta系数计算的期望收益之间的差额，业绩评价基准收益的总体波动性
    """

    def calculate_max_drawdown(self):
        temp = self.visual_account(self.threshold)
        final_balance = temp[0]
        cost = temp[7]
        balance = temp[1]
        initial_cost = temp[2]
        returns = balance / initial_cost
        alpha, beta = alpha_beta(returns, self.benchmark_returns)
        maxdrawdown = max_drawdown(returns)
        print("Balance: " + str(final_balance) + " Investment cost: " + str(cost))
        print('max drawdown = ' + str(maxdrawdown) + '; alpha = ' + str(alpha) + '; beta= ' + str(beta) + '.')
        return maxdrawdown, alpha, beta

    def plot_price_and_profit(self):
        temp = self.visual_account(self.threshold)
        bitcoin_price = temp[4]
        cum_profit = temp[3]
        time = temp[5]
        bitcoin_price = np.array(bitcoin_price)
        time = np.array(time)
        cum_profit = np.array(cum_profit)
        cum_profit = cum_profit.reshape(-1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(time, bitcoin_price, '-', label='bitcoin price')
        ax2 = ax.twinx()
        ax2.plot(time, cum_profit, '-r', label='profit')
        ax.set_xlabel('time')
        ax.set_ylabel('bitcoin price(yuan)')
        ax2.set_ylabel('profit(yuan)')
        plt.legend(loc='upper right', ncol=2)
        plt.grid(True)
        plt.show()

    def plot_threshold(self):
        threshold = np.arange(0.1, 0.2, 0.001).reshape(1, -1)
        temp = self.visual_account(threshold)
        pnl = np.array(temp[0]).reshape(1, -1)
        total_pnl = np.array(temp[1]).reshape(1, -1)
        plt.subplot(121)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(threshold, self.holding_time, '-b')
        ax.set_xlabel('threshold')
        ax.set_ylabel('holding time (blue)')
        ax2 = ax.twinx()
        ax2.plot(threshold, self.sample_size, '-k')
        ax2.set_ylabel('sample size (black)')

        plt.subplot(122)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(threshold, pnl, '-b')
        ax.set_xlabel('threshold')
        ax.set_ylabel('pnl (blue)')
        ax2 = ax.twinx()
        ax2.plot(threshold, total_pnl, '-k')
        ax2.set_ylabel('total pnl (black)')
        plt.show()

    def sharpe_ratio(self):
        trade_price = self.visual_account()[4]
        point = self.visual_account()[6]
        C = (trade_price[-1] - trade_price[1]) / (point[-1] - point[1])
        interval = []
        sum = np.sum(trade_price)
        mean = sum / len(trade_price)
        b = 0
        for i in range(len(trade_price) - 1):
            b += (trade_price[i] - mean) ** 2
        sharpe_ratio = (sum - C) / b
        return sharpe_ratio

    #if __name__ == '__main__':

