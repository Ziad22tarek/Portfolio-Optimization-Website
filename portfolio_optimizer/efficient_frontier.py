import pandas as pd
import numpy as np
from portfolio_optimizer.data_fetching import get_returns_df, get_statistical_summary
from portfolio_optimizer.portfolio_optimization import (
    get_max_sharp_ratio, get_minimum_variance,
    get_weights_for_target_return, get_portfolio_performance
)



def create_efficient_frontier(stock_list, mean_return, cov, risk_free_rate=0, number_of_portfolios=50):
    """
    Generate an efficient frontier of portfolios with varying levels of risk and return.

    Parameters:
    ---------------------
    stock_list : list
        List of stock symbols or names in the portfolio.
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.
    risk_free_rate : float, optional
        Risk-free rate (default is 0).
    number_of_portfolios : int, optional
        Number of portfolios to create on the efficient frontier (default is 50).

    Returns:
    ---------------------
    efficient_frontier_data : pd.DataFrame
        DataFrame containing efficient frontier data including portfolio weights, return, and standard deviation.

    """

    # Calculate maximum return and corresponding standard deviation for the efficient frontier
    max_sharpe_ratio, weights = get_max_sharp_ratio(mean_return, cov, risk_free_rate)
    max_return, max_return_std=get_portfolio_performance(weights,mean_return,cov)
    # Calculate minimum risk return and corresponding standard deviation for the efficient frontier
    min_variance, weights = get_minimum_variance(mean_return, cov)
    min_risk_return, min_std=get_portfolio_performance(weights,mean_return,cov)    # Create column headers for the DataFrame
    column_header = stock_list.copy()
    column_header.extend(['Return', 'Std','Sharpe Ratio'])
    
    # Initialize an empty DataFrame to store efficient frontier data
    efficient_frontier_data = pd.DataFrame(columns=column_header)
    
    # Generate a range of target returns for the efficient frontier
    target_returns = np.linspace(min_risk_return, 1, number_of_portfolios)
 
    # Iterate through each target return and calculate corresponding portfolio data
    for target_return in target_returns:
        # Get portfolio weights for the target return
        portfolio_return, weights = get_weights_for_target_return(mean_return, cov, target_return)
        
        # Calculate portfolio return and standard deviation
        Return, std = get_portfolio_performance(weights, mean_return, cov)
        sharpe_ratio=(Return-risk_free_rate)/std
        # Prepare a row of data containing weights, return, and standard deviation
        row = list(weights)
        row.extend([Return, std, sharpe_ratio])
        
        # Append the row to the efficient_frontier_data DataFrame
        efficient_frontier_data.loc[len(efficient_frontier_data)] = row

    return efficient_frontier_data






def generate_random_portfolios(columns,num_portfolios,stock_list,mean_return,cov,risk_free_rate=0):

    random_portfolios=pd.DataFrame(columns=columns)
    for _ in range(num_portfolios):
        random_weights = np.random.dirichlet(np.ones(len(stock_list)), size=1)
        Return, std=get_portfolio_performance(random_weights[0],mean_return,cov)
        sharpe_ratio=(Return-risk_free_rate)/std
        row=list(random_weights[0])
        row.extend([Return,std,sharpe_ratio])
        random_portfolios.loc[len(random_portfolios)]=row


    return random_portfolios




def create_optimal_points(efficient_frontier_columns,max_return,max_return_std,max_sharpe_ratio_weights,min_risk_return,min_std,min_variance_weights):
    optimal_points_columns=['Portfolio Type']
    optimal_points_columns.extend(efficient_frontier_columns)
    optimal_points=pd.DataFrame(columns=optimal_points_columns)
    max_sharpe_ratio_row=['Max Sharpe Ratio']
    max_sharpe_ratio_row.extend(max_sharpe_ratio_weights.round(3).tolist())
    max_sharpe_ratio_row.append(max_return.round(3))
    max_sharpe_ratio_row.append(max_return_std.round(3))
    max_sharpe_ratio_row.append((max_return/max_return_std).round(3))
    optimal_points.loc[len(optimal_points)]=max_sharpe_ratio_row
    min_variance_row=['Min Volatility']
    min_variance_row.extend(min_variance_weights.round(3).tolist())
    min_variance_row.append(min_risk_return.round(3))
    min_variance_row.append(min_std.round(3))
    min_variance_row.append((min_risk_return/min_std).round(3))
    optimal_points.loc[len(optimal_points)]=min_variance_row


    return optimal_points