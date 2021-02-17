import dash
import dash_core_components as dcc
import dash_html_components as html

from charts import backlog, forecast
from dash.dependencies import Input, Output
from datetime import date
from file_reader import parse_contents
from table import table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    html.Div([html.H3('Arquivo com as amostras')]),
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
    html.Div([html.H3('Data desejada para a entrega')]),
    html.Div([
        dcc.DatePickerSingle(
            id='deadline',
            min_date_allowed=date(2019, 1, 1),
            initial_visible_month=date(2021, 12, 25),
            date=date(2021, 12, 25),
            display_format='D/MM/YYYY'
        ),
        html.Div(id='output-container-date-picker-single')
    ]),
    html.Br(),
    html.Div([
        html.Div([html.H3('Total, ToDo and Done'),
                  dcc.Graph(id='iniciativa')]),
        html.Div([html.H3('Previsão'),
                  dcc.Graph(id='prediction')]),
    ],),
    html.Div([html.H3('Dados da Simulação')]),
    html.Div(id='output-data-upload'),
])

@app.callback([
    Output('iniciativa', 'figure'),
    Output('prediction', 'figure'),
    Output('output-data-upload', 'children')],
    [Input('upload-data', 'contents'), Input('upload-data', 'filename'), Input('deadline', 'date')])
def set_display_charts_and_table(contents, filename, deadline):
    if contents and filename and deadline:
        _df = parse_contents(contents, filename)
        if not _df is None:
            date_object = date.fromisoformat(deadline)
            date_string = date_object.strftime("%d/%m/%Y")
            _backlog, _df_backlog = backlog(_df)
            _forecast, _df_forecast = forecast(_df_backlog, date_string)
            if not _df_forecast is None:
                _table = table(_df_forecast, date_string)
                return _backlog, _forecast, _table
    return {'data': []}, {'data': []}, []

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug='True')
