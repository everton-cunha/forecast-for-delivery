import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from charts import backlog, forecast
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
from file_reader import parse_contents

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    html.Div([html.H3('Quando será que terminamos?')]),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arraste e Solte ou ',
            html.A('Selecione o arquivo')
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    html.Br(),
    html.Div([
        html.Div([html.H3('Total, ToDo and Done'),
                  dcc.Graph(id='iniciativa-carreta')]),
        html.Div([html.H3('Previsão'),
                  dcc.Graph(id='prediction-carreta')]),
    ],),
    html.Div([html.H3('Dados')]),
    html.Div(id='output-data-upload'),
])

########################################################


@app.callback([
    Output('iniciativa-carreta', 'figure'),
    Output('prediction-carreta', 'figure'),
    Output('output-data-upload', 'children')],
    [Input('upload-data', 'contents'), Input('upload-data', 'filename'), Input('upload-data', 'last_modified')])
def set_display_charts_and_table(contents, filename, last_modified):
    if contents and filename:
        _df = parse_contents(contents, filename)
        if not _df is None:
            _backlog, _df_backlog = backlog(_df)
            _forecast, _df_forecast = forecast(_df_backlog)
            data_columns = ['Data', 'ToDo', 'Done', 'Total','Pior caso', 'Melhor caso', 'Percentil 75', 'Percentil 50']
            df_columns = ['date', 'todo', 'done', 'total','worst', 'best', 'seventy_five', 'fifty']
            children = [html.Div([
                dash_table.DataTable(
                    data=_df_forecast.to_dict('records'),
                    columns=[{
                        'name': col, 
                        'id': df_columns[idx]
                    } for (idx, col) in enumerate(data_columns)],
                    css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                    style_cell={
                        'width': '{}%'.format(len(_df_forecast.columns)),
                        'textOverflow': 'ellipsis',
                        'overflow': 'hidden',
                        'textAlign': 'left',
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                ),
            ])]
            return _backlog, _forecast, children
    return {'data': []}, {'data': []}, []
########################################################


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
