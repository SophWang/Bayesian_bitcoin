import pandas as pd
from bayesian_model.data_processor import ProcessData
from bayesian_model.bayesian_regression import Prediction
from bayesian_model.performance_evaluation import Evaluation
from bayesian_model.index import Calculate_index
import numpy as np
import matplotlib.pyplot as plt


p1 = pd.read_csv('.//p1.csv')
p2 = pd.read_csv('.//p2.csv')
p3 = pd.read_csv('.//p3.csv')
# def read_data():
#p1 = pd.read_csv('.//price4.csv')
#p2 = pd.read_csv('.//price5.csv')
#p3 = pd.read_csv('.//price6.csv')
n = [90, 180, 360, 720]
price_reshaped_1 = p1.values.reshape((1, -1))[0, :]
price_reshaped_2 = p2.values.reshape((1, -1))[0, :]
price_reshaped_3 = p3.values.reshape((1, -1))[0, :]
data_pro = ProcessData(price_reshaped_1, n, 100, 20)
effective = data_pro.select_effective_clusters()
test_model = Prediction(effective, price_reshaped_2, n, price_reshaped_3)
p = test_model.predict_delta_p()
print(p)
actual_dp = []
for i in range(len(price_reshaped_3) - 1):
    actual_dp.append(price_reshaped_3[i + 1] - price_reshaped_3[i])
# print(actual_dp)
eval = Evaluation(price_reshaped_3, 720, p, 2, 0.07, True, 5000, 5000,100)
eval.plot_price_and_profit()
eval.correct_rate()
#eval.calculate_max_drawdown()
print(eval.sharpe_ratio())
    # delta = eval.visual_account()

returns=eval.periodic_return()[0]
market=eval.periodic_return()[1]
temp=Calculate_index(returns,market,0.05,0.04,1,500,4)
temp.test_risk_metrics()
temp.test_risk_adjusted_metrics()
print(eval.periodic_return())



#ts = data_pro.generate_time_series()
#cluster = data_pro.find_clusters()



#risk = eval.calculate_max_drawdown()
#print(risk)
#eval.calc_mean_return_by_quantile()

