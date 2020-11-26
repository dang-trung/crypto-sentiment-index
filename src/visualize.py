"""Visualization.

This module defines the function to plot the data-series versus each other in
pre-defined layouts.
"""
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


def plot_two_axis(data, series_1, series_2='',
                  name_series_1='', name_series_2=''):
    """
    Plot series 1 versus series 2 on two different axes with pre-defined
    layouts.

    Parameters
    ----------
    data : DataFrame
        Targeted dataset.
    series_1 : str
        Name of column (in the dataframe) for series 1.
    series_2 : str, optional
        Name of column (in the dataframe) for series 2. The default is '' 
        (i.e. no series 2).
    name_series_1 : str, optional
        Title for legends of series 1. The default is ''.
    name_series_2 : str, optional
        Title for legends of series 2. The default is ''.

    Returns
    -------
    NoneType.
        None. 
    """
    pio.renderers.default = 'browser'
    default_layout = go.Layout(font_family='Gravitas One',
                               xaxis_showgrid=False,
                               yaxis_showgrid=False,
                               showlegend=True,
                               legend_orientation='h',
                               legend_yanchor='bottom',
                               legend_y=1,
                               legend_xanchor='center',
                               legend_x=0.5)
    trace_main = go.Scatter(x=data.index, y=data[series_1], name=name_series_1,
                            marker_color='#FF6E58')
    if series_2 != "":
        fig = make_subplots(rows=1, cols=1, shared_xaxes=True,
                            specs=[[{'secondary_y': True}]])

        trace_sub = go.Scatter(x=data.index, y=data[series_2],
                               name=name_series_2, marker_color='#21CCCB')
        fig.add_trace(trace_main, secondary_y=False)
        fig.add_trace(trace_sub, secondary_y=True)
        fig['layout']['yaxis2']['showgrid'] = False
        fig.update_layout(default_layout)

    else:
        fig = go.Figure(trace_main, default_layout)

    return fig


def plot_same_axis(data, series_1, series_2='',
                   name_series_1='', name_series_2=''):
    """
    Plot series 1 versus series 2 on the same axis with pre-defined
    layouts.

    Parameters
    ----------
    data : DataFrame
        Targeted dataset.
    series_1 : str
        Name of column (in the dataframe) for series 1.
    series_2 : str, optional
        Name of column (in the dataframe) for series 2. The default is ''
        (i.e. no series 2).
    name_series_1 : str, optional
        Title for legends of series 1. The default is ''.
    name_series_2 : str, optional
        Title for legends of series 2. The default is ''.

    Returns
    -------
    NoneType.
        None.
    """
    pio.renderers.default = 'browser'
    default_layout = go.Layout(font_family='Gravitas One',
                               xaxis_showgrid=False,
                               yaxis_showgrid=False,
                               showlegend=True,
                               legend_orientation='h',
                               legend_yanchor='bottom',
                               legend_y=1,
                               legend_xanchor='center',
                               legend_x=0.5)
    trace_main = go.Scatter(x=data.index, y=data[series_1], name=name_series_1,
                            marker_color='#FF6E58')
    fig = go.Figure(trace_main, default_layout)
    if series_2 != "":
        trace_sub = go.Scatter(x=data.index, y=data[series_2],
                               name=name_series_2, marker_color='#21CCCB')
        fig.add_trace(trace_sub)
        fig.update_layout(default_layout)

    return fig
