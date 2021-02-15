import dash_html_components as html
import dash_table

def table(df_table, deadline):
    data_columns = ['Data', 'ToDo', 'Done', 'Total',
                    'Pior caso', 'Melhor caso', 'Percentil 75', 'Percentil 50']
    df_columns = ['date', 'todo', 'done', 'total',
                  'worst', 'best', 'seventy_five', 'fifty']
    table = [html.Div([
        dash_table.DataTable(
            data=df_table.to_dict('records'),
            columns=[{
                'name': col,
                'id': df_columns[idx]
            } for (idx, col) in enumerate(data_columns)],
            css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
            style_cell={
                'width': '{}%'.format(len(df_table.columns)),
                'textOverflow': 'ellipsis',
                'overflow': 'hidden',
                'textAlign': 'left',
            },
            style_data_conditional=(
                [
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ] +
                [
                    {
                        'if': {
                            'filter_query': '{{date}} = {}'.format(deadline),
                        },
                        'backgroundColor': '#FF4136',
                        'color': 'white'
                    },
                ]
            ),
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            }
        ),
    ])]

    return table
