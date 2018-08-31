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
{'Best n list': [100, 190, 370, 730], 'Best n_cluster': 95, 'Best n_effective': 16, 'Best step': 2, 'Best threshold': 0.001, 'Balance': 5378.0000062, 'sharpe ratio': 23.1978}   
Correct rate is: 0.62   
Bank balance: 5885.765   
final profit: 885.765   
return rate: 1.168   
borrowing capacity: 5000   
