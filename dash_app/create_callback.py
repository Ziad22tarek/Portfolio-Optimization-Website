from dash import Input, Output, State
from portfolio_optimizer.data_fetching import get_returns_df,get_statistical_summary
from portfolio_optimizer.data_visulization import plot_stocks_line_chart,plot_correlation_matrix,efficient_frontier_with_details,plot_stocks_vs_portfolio
from portfolio_optimizer.efficient_frontier import create_efficient_frontier,generate_random_portfolios,create_optimal_points
from portfolio_optimizer.portfolio_optimization import get_max_sharp_ratio,get_portfolio_performance,get_minimum_variance



def create_callback(app):
    """
    Create a callback function to update the figures and tables in the Dash app.

    Parameters:
        app (dash.Dash): The Dash app instance.

    Returns:
        function: The callback function for updating figures and tables.

    """

    @app.callback(
        [Output('Adj Close Figure Plot', 'figure'),
         Output('Correlation Figure', 'figure'),
         Output('efficient frontier figure', 'figure'),
         Output('Individual Stocks figure', 'figure'),
         Output('table-container', 'data'),
         Output('table-container', 'columns')],
        [Input('Calculate Button', 'n_clicks')],
        [State('Stocks Dropdown', 'value'),
         State('Date Picker', 'start_date'),
         State('Date Picker', 'end_date')],
        prevent_initial_call=True
    )
    def update(_, stock_list, start_date, end_date):
        """
        Update figures and tables based on user input.

        Parameters:
            _: n_clicks (not used)
            stock_list (list): List of selected stocks
            start_date (str): Start date of the selected period
            end_date (str): End date of the selected period

        Returns:
            tuple: Figures and data for the Dash components.
        """

        # Fetch returns DataFrame based on user input
        df = get_returns_df(stock_list, start_date, end_date)

        # Generate line chart for individual stocks
        stock_line_chart = plot_stocks_line_chart(df)

        # Calculate statistical summary
        mean_return, cov, corr, std, annualized_return, annualized_risk = get_statistical_summary(df)

        # Generate correlation matrix figure
        corr_fig = plot_correlation_matrix(corr)

        # Create efficient frontier data
        efficient_frontier_data = create_efficient_frontier(stock_list, mean_return, cov, number_of_portfolios=500)

        # Generate random portfolios for efficient frontier plot
        random_portfolios = generate_random_portfolios(efficient_frontier_data.columns, 2000, stock_list, mean_return, cov)

        # Calculate optimal portfolio points
        max_sharpe_ratio, max_sharpe_ratio_weights = get_max_sharp_ratio(mean_return, cov)
        max_return, max_return_std = get_portfolio_performance(max_sharpe_ratio_weights, mean_return, cov)
        min_variance, min_variance_weights = get_minimum_variance(mean_return, cov)
        min_risk_return, min_std = get_portfolio_performance(min_variance_weights, mean_return, cov)

        # Generate efficient frontier plot with key points
        efficient_frontier = efficient_frontier_with_details(
            max_return, max_return_std, max_sharpe_ratio, min_risk_return, min_std,
            min_risk_return/min_std, efficient_frontier_data['Return'], efficient_frontier_data['Std'],
            efficient_frontier_data['Sharpe Ratio'], random_portfolios['Return'], random_portfolios['Std'],
            random_portfolios['Sharpe Ratio']
        )

        # Generate plot comparing individual stocks with the portfolio
        individual_stocks_figure = plot_stocks_vs_portfolio(
            max_return, max_return_std, max_sharpe_ratio, min_risk_return, min_std, min_risk_return/min_std,
            efficient_frontier_data['Return'], efficient_frontier_data['Std'], efficient_frontier_data['Sharpe Ratio'],
            annualized_return, annualized_risk
        )

        # Create optimal points data for the table
        optimal_points = create_optimal_points(
            efficient_frontier_data.columns.to_list(), max_return, max_return_std, max_sharpe_ratio_weights,
            min_risk_return, min_std, min_variance_weights
        )

        data = optimal_points.to_dict('records')
        columns = [{"name": col, 'id': col} for col in optimal_points.columns]

        return stock_line_chart, corr_fig, efficient_frontier, individual_stocks_figure, data, columns
