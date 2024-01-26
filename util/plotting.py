import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

def plot_bar(df, filename, title, xlab, ylab, weight=None, disagg=False):

    if  disagg:
        fig = px.bar(df, x=xlab, y=ylab, title=title)

def _plot_bar_agg(df, filename, title, xlab, ylab):
    pass

def _plot_bar_disagg(df, filename, title, xlab, ylab):
    pass