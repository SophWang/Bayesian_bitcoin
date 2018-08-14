import numpy as np
from numpy.linalg import norm
from sklearn import linear_model
from decimal import *


class Prediction:

    def __init__(self, s, prices, n, price_3):
        self.prices = prices
        self.s = s
        self.n = n
        self.price_3 = price_3

    '''
    创建一个函数表示贝叶斯模型的公式
    '''
    def bayesian_model(self, x, center):
        num = 0
        den = 0
        getcontext().prec = 10
        getcontext().Emax = 99999999
        getcontext().Emin = -99999999

        for i in range(len(center)):
            x_i = center[i, :len(x)]
            y_i = center[i, len(x)]
            expect = np.exp(Decimal(-0.35 * norm(x - x_i) ** 2))
            num += expect * Decimal(y_i)
            den += expect
        return num/den

    '''
    建立delta_p和delta_p1,delta_p2,delta_p3之间的关系，并确定自变量X和应变量Y
    '''
    def variance_determine(self):
        X = np.empty((len(self.prices[0]) - max(self.n) - 1, 4))
        Y = np.empty((len(self.prices[0]) - max(self.n) - 1, 1))
        for i in range(max(self.n), len(self.prices[0]) - 1):

            delta_p = Decimal(self.prices[0, i+1]-self.prices[0, i])
            delta_p1 = self.bayesian_model(self.prices[0, i - self.n[0]:i], self.s[0][0])
            delta_p2 = self.bayesian_model(self.prices[0, i - self.n[1]:i], self.s[1][0])
            delta_p3 = self.bayesian_model(self.prices[0, i - self.n[2]:i], self.s[2][0])
            delta_p4 = self.bayesian_model(self.prices[0, i - self.n[3]:i], self.s[3][0])

            X[i - max(self.n), :] = [delta_p1, delta_p2, delta_p3, delta_p4]
            Y[i - max(self.n)] = delta_p

        return X, Y

    '''
    对第二个数据集中的X，Y进行线性拟合，确定参数w0, w1, w2, w3, w4
    '''
    def find_parameters_w(self):
        X, Y = self.variance_determine()
        clf = linear_model.LinearRegression()
        clf.fit(X, Y)
        w0 = clf.intercept_
        w1 = clf.coef_[0, 0]
        w2 = clf.coef_[0, 1]
        w3 = clf.coef_[0, 2]
        w4 = clf.coef_[0, 3]
        return w0, w1, w2, w3, w4

    '''
    利用拟合出的参数，根据XY的线性关系，求出各时点的价格变化，并储存在矩阵delta_p中
    '''
    def predict_delta_p(self):
        w0, w1, w2, w3, w4 = self.find_parameters_w()
        delta_p = []
        w0 = float(w0)
        for i in range(max(self.n), len(self.price_3[0])-1):
            delta_p1 = self.bayesian_model(self.price_3[0, i - self.n[0]:i], self.s[0][0])
            delta_p2 = self.bayesian_model(self.price_3[0, i - self.n[1]:i], self.s[1][0])
            delta_p3 = self.bayesian_model(self.price_3[0, i - self.n[2]:i], self.s[2][0])
            delta_p4 = self.bayesian_model(self.prices[0, i - self.n[3]:i], self.s[3][0])
            dp = Decimal(w0) + Decimal(w1) * delta_p1 + Decimal(w2) * delta_p2 + Decimal(w3) * delta_p3\
                 + Decimal(w4) * delta_p4
            delta_p.append(float(dp))
        return delta_p

    if __name__ == '__main__':
        import pandas as pd
        from bayesian.data_processor import ProcessData
        from bayesian.bayesian_regression import Prediction

        p1 = pd.read_csv('.//p1.csv')
        p2 = pd.read_csv('.//p2.csv')
        p3 = pd.read_csv('.//p3.csv')

        n = [90, 180, 360, 720]
        price_reshaped_1 = p1.values.reshape((1, -1))
        price_reshaped_2 = p2.values.reshape((1, -1))
        price_reshaped_3 = p3.values.reshape((1, -1))
        data_pro = ProcessData(price_reshaped_1, n, 100, 20)
        effective = data_pro.select_effective_clusters()
        test_model = Prediction(effective, price_reshaped_2, n, price_reshaped_3)
        p = test_model.predict_delta_p()
        print(p)
