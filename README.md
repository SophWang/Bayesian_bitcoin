# Bayesian_bitcoin

##  Bayesian linear regression model
### data source: https://www.kaggle.com/mikoim/bitcoin-historical-data
   - Bitcoin trading price that get recorded once per minute starting from 2016 to 2018.6
### Spliting the data set: 2/3 of the first 20k price data is training set, 1/3 is validation set, the following 20k data is test set

- Evaluation algorithm: set up a virtual account that trades according to the predicted price change, use the final bank balance and max drawdown to evaluate the model performance

- plot functions: plot_price_and_profit, plot_threshold_profit, plot_threshold_size
- evaluation functions imported from emperical package

### The following is the result of applying test data to the model:

![price and profit plot](https://github.com/SophWang/Bayesian_bitcoin/blob/master/bayesian_model/result.png)    
'Best n_list': [90, 180, 360], 'Best n_clusters': 100, 'Best n_effective': 16, 'Best step': 4, 'Best threshold': 0.005, 'Balance': 2202.8250000029802, 'Sharpe ratio': 0.002556140120108983   
Correct rate is: 0.5691056910569106   
cost =  65737.27499999998   
final profit:  855.069999999997   
Bank balance =  5855.069999999997   
return_rate =  0.1710139999999994   
vol = 0.11153125507168879   
beta = 0.7449634802008608   
CVaR(0.05) = 0.007610101010101099   
Drawdown = 0.15274082258955624   
Max Drawdown = 0.15274082258955624   
Treynor Ratio =0.013423476808962168   
Sharpe Ratio = 0.08966096538205649   
Information Ratio = 1.3276203145949916   
Excess VaR = 2.4777006937561588   
Conditional Sharpe Ratio = 1.3140430050437863   
Calmar Ratio = 0.06547038198734802   
Sterling Ratio = 0.10911730331224669   
Burke Ratio = 0.07319811231829398   

