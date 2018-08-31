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
{'Best n_list': [90, 180, 360], 'Best n_clusters': 100, 'Best n_effective': 16, 'Best step': 4, 'Best threshold': 0.005, 'Balance': 2202.825, 'Sharpe ratio': 0.0026}   
Correct rate is: 0.569 
cost =  65737.275   
final profit:  855.070   
Bank balance =  5855.070   
return_rate =  0.171   
vol = 0.112   
beta = 0.745   
CVaR(0.05) = 0.0076   
Drawdown = 0.1527   
Max Drawdown = 0.1527   
Treynor Ratio =0.0134   
Sharpe Ratio = 0.0897   
Information Ratio = 1.328   
Excess VaR = 2.478   
Conditional Sharpe Ratio = 1.314   
Calmar Ratio = 0.065   
Sterling Ratio = 0.109   
Burke Ratio = 0.0731   

