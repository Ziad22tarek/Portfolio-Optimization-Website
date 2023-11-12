import yfinance as yf
import pandas as pd
import numpy as np
from .portfolio_optimization import get_portfolio_performance



def get_returns_df(tickers, start_date=None,end_date=None):
    '''get the returns data of tickers you want 



    Parameters
    ---------------------
    tickers: list
        a list of symbols of the stocks
    start_date: str
        start date you want to get the data from, and it suppose to be in that format (YYYY-MM-DD)


    Returns
    -------------------------
    A Pandas DataFrame with your desired data
    '''

    df = yf.download(tickers, start=start_date,end=end_date)['Adj Close']
    return df


def get_statistical_summary(df):
    '''get the return and the covariance matriex of stock returns

    Parameters
    ------------------
    df: pandas.DataFrame
        A pandas DataFrame of the Adjusted close of your desired stocks


    Return
    -------------------

    meanreturns: pandas.series
        A Pandas Series of the mean return of each stock
    cov: pandas.DataFrame
        A covariance matrix of the stocks'''

    # calculate the returns os the stock
    returns = df.pct_change()
    # calculate the mean of returns
    meanreturns = returns.mean()
    # calculate the covariance matrix
    cov = returns.cov()

    corr=returns.corr()

    std=returns.std()

    annualized_return = (1 + meanreturns)**252 - 1

    annualized_risk = std * (252**0.5)

    return meanreturns, cov,corr,std,annualized_return,annualized_risk



def generate_random_protfolios(stock_list,mean_return,cov,no_portfolios=2000,risk_free_rate=0):
    

    column_header=stock_list
    column_header.extend(['Return', 'Std','Sharpe Ratio'])
    random_portfolios=pd.DataFrame(columns=column_header)
    for _ in range(no_portfolios):
        random_weights = np.random.dirichlet(np.ones(len(stock_list)), size=1)
        Return, std=get_portfolio_performance(random_weights[0],mean_return,cov)
        sharpe_ratio=(Return-risk_free_rate)/std
        row=list(random_weights[0])
        row.extend([Return,std,sharpe_ratio])
        random_portfolios.loc[len(random_portfolios)]=row


    return random_portfolios


    



