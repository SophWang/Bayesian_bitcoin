import math
import numpy
import numpy.random as nrand
from empyrical import max_drawdown, alpha_beta


class Calculate_index(object):
    def __init__(self, returns,  market, er, rf, threshold, investment, periods, alpha):
        self.returns = returns
        self.market = market
        self.er = er
        self.rf = rf
        self.threshold = threshold
        self.investment=investment
        self.periods = periods
        self.alpha=alpha


    def vol(self):
        # Return the standard deviation of returns
        return numpy.std(self.returns)

    def alpha_beta(self):
        final_return = numpy.array(self.returns)
        benchmark = numpy.array(self.market)
        alpha, beta = alpha_beta(final_return, benchmark)
        return alpha, beta

    '''
    partial moment
    '''

    '''
    def lpm(self, returns, threshold, order):
        # This method returns a lower partial moment of the returns
        # Create an array the same length as returns containing the minimum return threshold
        threshold_array = numpy.empty(len(returns))
        threshold_array.fill(threshold)
        # Calculate the difference between the threshold and the returns
        diff = threshold_array - returns
        # Set the minimum of each to 0
        diff = diff.clip(min=0)
        # Return the sum of the different to the power of order
        return numpy.sum(diff ** order) / len(returns)


    def hpm(self, returns, threshold, order):
        # This method returns a higher partial moment of the returns
        # Create an array he same length as returns containing the minimum return threshold
        threshold_array = numpy.empty(len(returns))
        threshold_array.fill(threshold)
        # Calculate the difference between the returns and the threshold
        diff = returns - threshold_array
        # Set the minimum of each to 0
        diff = diff.clip(min=0)
        # Return the sum of the different to the power of order
        return numpy.sum(diff ** order) / len(returns)

    '''
    '''
    var
    '''

    def var(self):
        # This method calculates the historical simulation var of the returns
        #alpha=self.alpha_beta()[0]
        sorted_returns = numpy.sort(self.returns)
        # Calculate the index associated with alpha
        index = int(self.alpha * len(sorted_returns))
        # VaR should be positive
        return abs(sorted_returns[index])

    def cvar(self):
        #alpha = self.alpha_beta()[0]
        # This method calculates the condition VaR of the returns
        sorted_returns = numpy.sort(self.returns)
        # Calculate the index associated with alpha
        index = self.alpha * len(sorted_returns)
        # Calculate the total VaR beyond alpha
        sum_var = sorted_returns[0]
        for i in range(1, int(index)):
            sum_var += sorted_returns[i]
        # Return the average VaR
        # CVaR should be positive
        return abs(sum_var / index)

    '''
    drawdown
    '''

    def prices(self):
        # Converts returns into prices
        s = [self.investment]
        for i in range(len(self.returns)):
            s.append(self.investment * (1 + self.returns[i]))
        return numpy.array(s)

    def dd(self):
        # Returns the draw-down given time period tau
        values = self.prices()
        pos = len(values) - 1
        pre = pos - self.periods
        drawdown = 50
        # Find the maximum drawdown given tau
        while pre >= 0:
            dd_i = (values[pos] / values[pre]) - 1
            if dd_i < drawdown:
                drawdown = dd_i
            pos, pre = pos - 1, pre - 1
        # Drawdown should be positive
        return abs(drawdown)

    def max_dd(self):
        # Returns the maximum draw-down for any tau in (0, T) where T is the length of the return series
        max_drawdown = float('-inf')
        for i in range(0, len(self.returns)):
            drawdown_i = self.dd()
            if drawdown_i > max_drawdown:
                max_drawdown = drawdown_i
        # Max draw-down should be positive
        return abs(max_drawdown)

    def average_dd(self):
        # Returns the average maximum drawdown over n periods
        drawdowns = []
        for i in range(0, len(self.returns)):
            drawdown_i = self.dd()
            drawdowns.append(drawdown_i)
        drawdowns = sorted(drawdowns)
        total_dd = abs(drawdowns[0])
        for i in range(1, self.periods - 2):
            total_dd += abs(drawdowns[i])
        return total_dd / self.periods

    def average_dd_squared(self):
        # Returns the average maximum drawdown squared over n periods
        drawdowns = []
        for i in range(0, len(self.returns)):
            drawdown_i = math.pow(self.dd(), 2.0)
            drawdowns.append(drawdown_i)
        drawdowns = sorted(drawdowns)
        total_dd = abs(drawdowns[0])
        for i in range(0, self.periods - 2):
            total_dd += abs(drawdowns[i])
        return total_dd / self.periods

    '''
    risk-adjust return based on volatility
    '''

    def treynor_ratio(self):
        result = (self.er - self.rf) / self.alpha_beta()[1]
        return result

    def sharpe_ratio(self):
        result = (self.er - self.rf) / self.vol()
        return result

    def information_ratio(self):
        benchmark = numpy.array(self.market)
        diff = self.returns - benchmark
        return numpy.mean(diff) / self.vol()

    def modigliani_ratio(self):
        benchmark = numpy.array(self.market)
        np_rf = numpy.empty(len(self.returns))
        np_rf.fill(self.rf)
        rdiff = self.returns - np_rf
        bdiff = benchmark - np_rf
        return (self.er - self.rf) * (self.vol(rdiff) / self.vol(bdiff)) + self.rf

    '''
    risk-adjust return based on var
    '''

    def excess_var(self):
        #alpha=self.alpha_beta()[0]
        return (self.er - self.rf) / self.var()

    def conditional_sharpe_ratio(self):
        #alpha = self.alpha_beta()[0]
        return (self.er - self.rf) / self.cvar()

    '''
    risk-adjust return based on partial moment
    

    def omega_ratio(self,  target=0):
        return (self, self.er - self.rf) / self.lpm(self.returns, target, 1)

    def sortino_ratio(self,  target=0):
        return (self.er - self.rf) / math.sqrt(self.lpm(self.returns, target, 2))

    def kappa_three_ratio(self,  target=0):
        return (self.er - self.rf) / math.pow(self.lpm(self.returns, target, 3), float(1 / 3))

    def gain_loss_ratio(self,  target=0):
        return self.hpm(self.returns, target, 1) / self.lpm(self.returns, target, 1)

    def upside_potential_ratio(self,  target=0):
        return self.hpm(self.returns, target, 1) / math.sqrt(self.lpm(self.returns, target, 2))
    '''
    '''
    risk-adjust return based on drawdown
    '''

    def calmar_ratio(self):
        return (self.er - self.rf) / self.max_dd()

    def sterling_ration(self):
        return (self.er - self.rf) / self.average_dd()

    def burke_ratio(self):
        return (self.er - self.rf) / math.sqrt(self.average_dd_squared())

    def test_risk_metrics(self):
        # This is just a testing method
        r = nrand.uniform(-1, 1, 50)
        m = nrand.uniform(-1, 1, 50)
        print("vol =", self.vol())
        print("beta =", self.alpha_beta()[1])
        #print("hpm(0.0)_1 =", self.hpm(r, 0.0, 1))
        #print("lpm(0.0)_1 =", self.lpm(r, 0.0, 1))
        #print("VaR(0.05) =", self.var())
        print("CVaR(0.05) =", self.cvar())
        print("Drawdown =", self.dd())
        print("Max Drawdown =", self.max_dd())

    def test_risk_adjusted_metrics(self):
        # Returns from the portfolio (r) and market (m)
        r = nrand.uniform(-1, 1, 50)
        m = nrand.uniform(-1, 1, 50)
        # Expected return
        e = numpy.mean(r)
        # Risk free rate
        f = 0.06
        # Risk-adjusted return based on Volatility
        temp = self.treynor_ratio()
        print("Treynor Ratio =" + str(temp))  # 每单位风险获得的风险溢价#
        print("Sharpe Ratio =", self.sharpe_ratio())
        print("Information Ratio =", self.information_ratio())  # 单位主动风险所带来的超额收益。#
        # Risk-adjusted return based on Value at Risk
        print("Excess VaR =", self.excess_var())
        print("Conditional Sharpe Ratio =", self.conditional_sharpe_ratio())
        # Risk-adjusted return based on Lower Partial Moments
        #print("Omega Ratio =", self.omega_ratio(e, r, f))  #
        #print("Sortino Ratio =", self.sortino_ratio(e, r, f))
        #print("Kappa 3 Ratio =", self.Omega_Ratio(e, r, f))
        #print("Gain Loss Ratio =", self.gain_loss_ratio(r))
        #print("Upside Potential Ratio =", self.upside_potential_ratio(r))
        # Risk-adjusted return based on Drawdown risk
        print("Calmar Ratio =", self.calmar_ratio())
        print("Sterling Ratio =", self.sterling_ration())
        print("Burke Ratio =", self.burke_ratio())

    if __name__ == "__main__":
        from bayesian_model.index import Calculate_index
        test = Calculate_index([0,1,2,3], [1,2,3,4], 1, 1, 1,5000,5,0.05)
        risk_metrics = test.test_risk_metrics()
        risk_adjusted_metrics=test.test_risk_adjusted_metrics()
        #test_risk_metrics()
        #test_risk_adjusted_metrics()
