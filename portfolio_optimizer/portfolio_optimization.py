import numpy as np
import scipy.optimize as sc






def get_portfolio_performance(weights, mean_return, cov):
    '''Calculating the portfolio performance

    Parameters
    --------------------------
    weights: np.array
        the weights for each stock in the portfolio

    mean_return: np.array
        the mean return for each stock

    cov: np.array
        the covariance matrix of the stocks in the portfolio 
    Returns
    ----------------------------
    p_return: float
        the return of the portfolio

    p_std: float
        the std of thr portfolio
     '''

    p_return = np.sum(mean_return*weights)*252
    p_std = 0.5*np.sqrt(np.dot(weights.T, np.dot(cov, weights)))*np.sqrt(252)

    return p_return, p_std


def negative_sharpe_ratio(weights, mean_return, cov, risk_free_rate=0):
    """
    Calculate the negative of the Sharpe ratio for a given portfolio.

    Parameters:
    ---------------------
    weights : np.array
        Portfolio weights for each asset.
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.
    risk_free_rate : float, optional
        Risk-free rate (default is 0).

    Returns:
    ---------------------
    negative_sharpe : float
        Negative of the Sharpe ratio.
    """

    p_return, p_std = get_portfolio_performance(weights, mean_return, cov)

    if p_std == 0:
        # Return a large negative value to indicate an infeasible portfolio
        negative_sharpe = -1e10
    else:
        negative_sharpe = -((p_return - risk_free_rate) / p_std)

    return negative_sharpe


def minimum_variance(weights, mean_return, cov):
    """
    Calculate the portfolio standard deviation (risk) for a given set of weights.

    Parameters:
    ---------------------
    weights : np.array
        Portfolio weights for each asset.
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.

    Returns:
    ---------------------
    portfolio_stddev : float
        Portfolio standard deviation (risk).
    """

    p_return, p_std = get_portfolio_performance(weights, mean_return, cov)
    portfolio_stddev = p_std

    return portfolio_stddev


def get_max_sharp_ratio(mean_return, cov, risk_free_rate=0):
    """
    Find the maximum Sharpe ratio portfolio weights.

    Parameters:
    ---------------------
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.
    risk_free_rate : float, optional
        Risk-free rate (default is 0).

    Returns:
    ---------------------
    max_sharpe_ratio : float
        Maximum Sharpe ratio.
    weights : np.array
        Portfolio weights for the maximum Sharpe ratio.
    """

    # Initialize equal weights for each asset in the portfolio
    initial_weights = [1. / len(mean_return)] * len(mean_return)

    # Prepare arguments for the negative_sharpe_ratio function
    args = (mean_return, cov, risk_free_rate)

    # Define equality constraint to ensure sum of weights equals 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Define bounds for portfolio weights (between 0 and 1)
    bounds = tuple((0, 1) for asset in range(len(mean_return)))

    # Minimize the negative of Sharpe ratio using SLSQP method
    results = sc.minimize(negative_sharpe_ratio, initial_weights,
                          args, method='SLSQP', bounds=bounds, constraints=constraints)

    # Extract the maximum Sharpe ratio and corresponding weights
    max_sharpe_ratio, weights = -results['fun'], results['x']

    return max_sharpe_ratio, weights


def get_minimum_variance(mean_return, cov):
    """
    Find the portfolio weights that correspond to the minimum variance.

    Parameters:
    ---------------------
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.

    Returns:
    ---------------------
    min_variance : float
        Minimum portfolio variance.
    weights : np.array
        Portfolio weights for the minimum variance.
    """

    # Initialize equal weights for each asset in the portfolio
    initial_weights = [1. / len(mean_return)] * len(mean_return)

    # Prepare arguments for the minimum_variance function
    args = (mean_return, cov)

    # Define equality constraint to ensure sum of weights equals 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

    # Define bounds for portfolio weights (between 0 and 1)
    bounds = tuple((0, 1) for asset in range(len(mean_return)))

    # Minimize the portfolio standard deviation using SLSQP method
    results = sc.minimize(minimum_variance, initial_weights, args,
                          method='SLSQP', bounds=bounds, constraints=constraints)

    # Extract the minimum portfolio variance and corresponding weights
    min_variance, weights = results['fun'], results['x']

    return min_variance, weights


def portfolioReturn(weights, mean_return, cov):
        return get_portfolio_performance(weights, mean_return, cov)[0]

def portfolioVariance(weights, mean_return, cov):
        return get_portfolio_performance(weights, mean_return, cov)[1]

def get_weights_for_target_return(mean_return, cov, return_target):
    """
    Find portfolio weights for a given target return while ensuring the weights sum to 1.

    Parameters:
    ---------------------
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.
    return_target : float
        Target portfolio return.

    Returns:
    ---------------------
    portfolio_return : float
        Achieved portfolio return.
    weights : np.array
        Portfolio weights for the target return.
    """

    # Initialize equal weights for each asset in the portfolio
    initial_weights = [1. / len(mean_return)] * len(mean_return)
    
    # Prepare arguments for the portfolioReturn function
    args = (mean_return, cov)
    
    # Define equality constraint to ensure sum of weights equals 1
    # and inequality constraint for achieving target return
    constraints = ({'type': 'eq', 'fun': lambda x: portfolioReturn(x, mean_return, cov) - return_target},
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        
    )
    
    # Define bounds for portfolio weights (between 0 and 1)
    bounds = tuple((0, 1) for asset in range(len(mean_return)))
    
    # Minimize the portfolio return using SLSQP method
    results = sc.minimize(portfolioVariance, initial_weights, args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    
    portfolio_return, weights = results['fun'], results['x']

    return portfolio_return, weights










def get_weights_for_target_variance(mean_return, cov, variance_target):
    """
    Find portfolio weights for a given target portfolio variance while ensuring the weights sum to 1.

    Parameters:
    ---------------------
    mean_return : np.array
        Mean return for each asset.
    cov : np.array
        Covariance matrix of asset returns.
    variance_target : float
        Target portfolio variance.

    Returns:
    ---------------------
    portfolio_variance : float
        Achieved portfolio variance.
    weights : np.array
        Portfolio weights for the target variance.
    """

    # Initialize equal weights for each asset in the portfolio
    initial_weights = [1. / len(mean_return)] * len(mean_return)
    
    # Prepare arguments for the portfolioVariance function
    args = (mean_return, cov)
    
    # Define equality constraint to ensure sum of weights equals 1
    # and inequality constraint for achieving target variance
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: variance_target - portfolioVariance(x, mean_return, cov)}
    )
    
    # Define bounds for portfolio weights (between 0 and 1)
    bounds = tuple((0, 1) for asset in range(len(mean_return)))
    
    # Minimize the portfolio variance using SLSQP method
    results = sc.minimize(portfolioVariance, initial_weights, args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
    
    portfolio_variance, weights = results['fun'], results['x']

    return portfolio_variance, weights