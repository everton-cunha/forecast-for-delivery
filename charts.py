import os
import pandas as pd
import plotly.graph_objs as go

from forecasting import forecasting

def backlog(df):
    df['total'] = df['done'] + df['todo']
    trace1 = go.Bar(
        x=df['date'],
        y=df['done'],
        name='Done',
        text=df['done'],
        textposition='inside',
        marker=dict(color='#2E8B57')
    )

    trace2 = go.Bar(
        x=df['date'],
        y=df['todo'],
        name='To Do',
        text=df['todo'],
        textposition='inside',
        marker=dict(color='#8FBC8F')
    )

    trace3 = go.Scatter(
        x=df['date'],
        y=df['total'],
        mode='lines+markers+text',
        name='Total',
        text=df['total'],
        textposition='top center',
        marker=dict(color='#17BECF')
    )

    data = [trace1, trace2, trace3]
    layout = go.Layout(barmode='stack', plot_bgcolor='white')

    fig = go.Figure(data=data, layout=layout)
    return fig, df


def forecast(df_file, deadline):
    df = forecasting(df_file)
    if not df is None:
        cone1 = go.Scatter(
            x=df['date'],
            y=df['done'],
            mode='lines+markers+text',
            name='Done',
            text=df['done'],
            textposition='bottom center',
            marker=dict(color='#17BECF')
        )

        cone2 = go.Scatter(
            x=df['date'],
            y=df['total'],
            mode='lines+markers+text',
            name='Total',
            text=df['total'],
            textposition='top center',
            marker=dict(color='#581845')
        )

        cone3 = go.Scatter(
            x=df['date'],
            y=df['best'],
            mode='lines+markers+text',
            name='Melhor Caso',
            text=df['best'],
            textposition='bottom center',
            marker=dict(color='#119E19')
        )

        cone4 = go.Scatter(
            x=df['date'],
            y=df['seventy_five'],
            mode='lines+markers+text',
            name='Provável (percentil 75)',
            text=df['seventy_five'],
            textposition='bottom center',
            marker=dict(color='#FF8C00')
        )
    
        cone5 = go.Scatter(
            x=df['date'],
            y=df['fifty'],
            mode='lines+markers+text',
            name='Provável (percentil 50)',
            text=df['fifty'],
            textposition='bottom center',
            marker=dict(color='#FCBD00')
        )

        cone6 = go.Scatter(
            x=df['date'],
            y=df['worst'],
            mode='lines+markers+text',
            name='Pior Caso',
            text=df['worst'],
            textposition='bottom center',
            marker=dict(color='#D5230B')
        )

        data = [cone1, cone2, cone3, cone4, cone5, cone6]

        layout = go.Layout(plot_bgcolor='white')
        fig = go.Figure(data=data, layout=layout)

        fig.add_vrect(
            x0=deadline, x1=df['date'].iloc[-1],
            fillcolor="LightSalmon", opacity=0.5,
            layer="below", line_width=0,
        )

        fig.add_vrect(
            x0=df['date'].iloc[0], x1=deadline,
            fillcolor="LightGreen", opacity=0.5,
            layer="below", line_width=0,
        )

        return fig, df
    return None, None
