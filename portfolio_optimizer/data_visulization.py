import plotly.express as px
import plotly.graph_objects as go


def color_map():
    """
    Returns a list of professional hex colors for line chart color mapping.
    
    Returns:
    ---------------------
    professional_hex_colors : list
        List of professional hex colors.
    """
    professional_hex_colors = [
    '#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
    '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
    '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
    '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5',
    '#5254a3', '#8c6d31', '#9c9ede', '#d3d3d3', '#d6616b',
    '#e6550d', '#fdd0a2', '#e7ba52', '#31a354', '#74c476',
    '#a1d99b', '#756bb1', '#bcbddc', '#969696', '#6baed6',
    '#c6dbef', '#9ecae1', '#6b6ecf', '#e377c2', '#f7b6d2',
    '#7b4173', '#a55194', '#ce6dbd', '#de9ed6', '#8c6d31',
    '#bd9e39', '#e7ba52', '#ad494a', '#d6616b', '#91003f'
    ]
    return professional_hex_colors

   
def hover_template():
    """
    Define the hover template for hover tooltips.

    Returns:
    ----------------
    template : str
        Hover template with placeholders.
    """
    template = 'Annualized Return (%): %{y}<br>Annualized Volatility (%): %{x}<br>Sharpe Ratio: %{text}<extra></extra>'
    return template


def plot_stocks_line_chart(data):
    """
    Plot a line chart for stocks' adjusted close prices.
    
    Parameters:
    ---------------------
    data : pandas.DataFrame
        DataFrame containing stocks' adjusted close prices with dates as the index and stock symbols as columns.
        
    Returns:
    ---------------------
    stock_line_chart : plotly.graph_objs._figure.Figure
        Plotly figure object for the line chart.
    """

    # Customize legend appearance
    legend = dict(
        title='Companies Symbols',
        bgcolor="#ECECF0",
        bordercolor="#ECECF0",
        borderwidth=0,
        x=1,
        y=1,
    )

    # Customize font appearance
    font = dict(
        family="Arial",
        size=12,
        color="black",
    )

    # Create a line chart with Plotly Express
    stock_line_chart = px.line(data,
                               x=data.index,
                               y=data.columns,
                               color_discrete_sequence=color_map()
                               )

    # Update layout settings
    stock_line_chart.update_layout(
        # Titles
        title='Stocks Adj Close price through the period',
        xaxis_title="Date",
        yaxis_title='Adj Close Price',
        # Layout colors
        plot_bgcolor="white",
        paper_bgcolor="white",
        # Grids
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        # Figure Size
        #width=1150,
        #height=700,
        # Legend
        legend=legend,
        font=font,
        xaxis=dict(
        rangeselector=dict(
            buttons=[
                dict(count=6, label='6m', step='month', stepmode='backward'),
                dict(count=1, label='YTD', step='year', stepmode='todate'),
                dict(count=1, label='1y', step='year', stepmode='backward'),
                dict(count=2, label='2y', step='year', stepmode='backward'),
                dict(count=3, label='3y', step='year', stepmode='backward'),
                dict(step='all')
            ],
            bgcolor='rgba(0,46,69,0.5)',  # Set background color of the buttons
            font=dict(color='white'),
            x=0,  # Adjust the horizontal position (0 to 1)
            y=1
        ),
        type='date'  # Set the x-axis type to date
    ),
    )

    return stock_line_chart







def plot_correlation_matrix(corr):
    """
    Plots the correlation matrix of portfolio assets as a heatmap.

    Parameters:
    ----------------------------
        corr : pandas.DataFrame
            The correlation matrix.

    Returns:
    -----------------------------
        fig : plotly.graph_objs._figure.Figure
            The Plotly figure object.
    """

    # Create a heatmap plot using Plotly Express
    fig = px.imshow(corr,
                    x=corr.index,
                    y=corr.columns,
                    color_continuous_scale="Blues",
                   )

    # Update layout to customize the appearance
    fig.update_layout(
        title='Correlation Matrix of Portfolio Assets',
        width=600,
    )

    return fig





def create_single_point_plot(point_name, x_value, y_value,sharpe_ratio=0,with_border=True):
    """
    Create a scatter plot with a single point marker and return it.

    Parameters:
    ----------------
    point_name : str
        Name or label for the point.

    x_value : float
        X-coordinate of the point.

    y_value : float
        Y-coordinate of the point.

    Returns:
    ----------------
    point : plotly.graph_objs._scatter.Scatter
        Scatter plot object representing the point.
    """
    hovertemplate = f'Name: {point_name}'+"<br>Annualized Return (%): %{y}<br>Annualized Volatility (%): %{x}<br>Sharpe Ratio: "+f'{sharpe_ratio}'+"<extra></extra>"
    if with_border:
        marker=dict(color='blue', size=14, line=dict(color='black', width=2))
    else:
        marker=dict(color='red')
    # Create a scatter plot for the given point
    point = go.Scatter(
        name=point_name,
        x=[x_value],
        y=[y_value],
        mode='markers',
        marker=marker,
        text=sharpe_ratio,
        hovertemplate=hovertemplate

    )

    return point




def plot_efficient_frontier(Return, STD, Sharpe_Ratio):
    """
    Plot the Efficient Frontier curve.

    Parameters:
    ----------------
    Return : list
        List of annualized returns.

    STD : list
        List of annualized volatilities (standard deviations).

    Sharpe_Ratio : list
        List of Sharpe ratios.

    Returns:
    ----------------
    efficient_frontier_graph : plotly.graph_objs._scatter.Scatter
        Scatter plot representing the Efficient Frontier.
    """
    efficient_frontier_graph = go.Scatter(
        name='Efficient Frontier',
        mode='lines',
        y=Return,
        x=STD,
        line=dict(color='black', width=2),
        text=Sharpe_Ratio,
        hovertemplate=hover_template(),
    )
    return efficient_frontier_graph


def efficient_frontier_with_details(
    max_return, max_return_std, max_sharpe_ratio,
    min_volatility_return, min_volatility, min_volatility_sharpe_ratio,
    Return, STD, Sharpe_Ratio,
    random_portfolios_return, random_portfolios_std, random_portfolios_sharpe_ratio
):
    """
    Create a portfolio optimization plot with Efficient Frontier and key points.

    Parameters:
    ----------------
    max_return : float
        Maximum return achieved.

    max_return_std : float
        Volatility corresponding to maximum return.

    max_sharpe_ratio : float
        Sharpe ratio at maximum return.

    min_volatility_return : float
        Return at the global minimum volatility.

    min_volatility : float
        Global minimum volatility achieved.

    min_volatility_sharpe_ratio : float
        Sharpe ratio at the global minimum volatility point.

    Return : list
        List of annualized returns.

    STD : list
        List of annualized volatilities (standard deviations).

    Sharpe_Ratio : list
        List of Sharpe ratios.

    random_portfolios_return : list
        List of random portfolios' returns.

    random_portfolios_std : list
        List of random portfolios' volatilities.

    random_portfolios_sharpe_ratio : list
        List of Sharpe ratios for random portfolios.

    Returns:
    ----------------
    figure : plotly.graph_objs._figure.Figure
        Plotly figure displaying Efficient Frontier and key points.
    """
    layout = go.Layout(
        title='Portfolio Optimization with Efficient Frontier',
        yaxis_title='Annualized Return (%)',
        xaxis_title='Annualized Volatility (%)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        #width=1150,
        #height=600,
        xaxis=dict(linecolor='black'),
        yaxis=dict(linecolor='black'),
        legend=dict(
            x=1.3,
            y=1.1,
            xanchor='left',
            bgcolor='#FFFFE0',
        ),
    )

    max_ratio_point = create_single_point_plot(
        point_name='Maximum Sharpe Ratio',
        x_value=max_return_std,
        y_value=max_return,
        sharpe_ratio=max_sharpe_ratio,
    )

    global_minimum = create_single_point_plot(
        point_name='Global Minimum',
        x_value=min_volatility,
        y_value=min_volatility_return,
        sharpe_ratio=min_volatility_sharpe_ratio,
    )

    efficient_frontier = plot_efficient_frontier(Return, STD, Sharpe_Ratio)

    random_portfolios_graph = go.Scatter(
        name='Portfolios',
        mode='markers',
        y=random_portfolios_return,
        x=random_portfolios_std,
        text=random_portfolios_sharpe_ratio,
        hovertemplate=hover_template(),
        marker=dict(
            color=random_portfolios_sharpe_ratio,
            colorbar=dict(
                title='Sharpe Ratio',
                titleside='right',
                ticks='outside',
            ),
            colorscale='YlGnBu',
        ),
    )

    figure = go.Figure(
        data=[random_portfolios_graph, efficient_frontier, max_ratio_point, global_minimum],
        layout=layout,
    )

    return figure


def plot_stocks_vs_portfolio(max_return, max_return_std, max_sharpe_ratio,
    min_volatility_return, min_volatility, min_volatility_sharpe_ratio,
    Return, STD, Sharpe_Ratio,annualized_return,annualized_risk):


    layout = go.Layout(
        title='Portfolio Optimization with Individual Stocks',
        yaxis_title='Annualized Return (%)',
        xaxis_title='Annualized Volatility (%)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        #width=1150,
        #height=600,
        xaxis=dict(linecolor='black'),
        yaxis=dict(linecolor='black'),
        legend=dict(
            x=1.3,
            y=1.1,
            xanchor='left',
            bgcolor='#FFFFE0',
        ),
    )

    max_ratio_point = create_single_point_plot(
        point_name='Maximum Sharpe Ratio',
        x_value=max_return_std,
        y_value=max_return,
        sharpe_ratio=max_sharpe_ratio,
    )

    global_minimum = create_single_point_plot(
        point_name='Global Minimum',
        x_value=min_volatility,
        y_value=min_volatility_return,
        sharpe_ratio=min_volatility_sharpe_ratio,
    )
    efficient_frontier = plot_efficient_frontier(Return, STD, Sharpe_Ratio)


    data=[create_single_point_plot(annualized_return.index[i],annualized_risk[i],annualized_return[i],(annualized_return[i]/annualized_risk[i]),with_border=False) for i in range(len(annualized_return))]

    data.extend([efficient_frontier,max_ratio_point,global_minimum])

    figure = go.Figure(data=data,layout=layout)


    return figure




