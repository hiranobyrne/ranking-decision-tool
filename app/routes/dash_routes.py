import os
import pandas as pd
from dash import Dash, html, dash_table


def create_dash_app(flask_app):
    dataset = 'ahp_cars.csv'
    data_dir = os.path.join(flask_app.root_path, '../data/csv_datasets')
    csv_file_path = os.path.join(data_dir, dataset)

    df = pd.read_csv(csv_file_path)

    # initialize Dash app
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash/'
    )

    # Dash layout
    dash_app.layout = html.Div([
        # html.H1('Dataset'),
        dash_table.DataTable(
            id='datatable',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
        )
    ])

    return dash_app
