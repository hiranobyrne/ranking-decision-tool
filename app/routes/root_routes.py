from flask import render_template, current_app, Blueprint

# import pandas as pd
from app.routes import main
# from app.utils.utils import get_timestamp
# import dash
# from dash import html, dash_table
from flask import flash, render_template, request, current_app, redirect, url_for, session
# import os
import pandas as pd


main = Blueprint('main', __name__)


# @main.route('/')
# def index():
#      # print(">>> ahp_dataset_selection()")
#
#     # busca o path dos dados que estah em config.py
#     data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
#
#     # print(">>> ahp_dataset_selection.data_dir:", data_dir)
#
#     # busca todos csv na diretoria dos dados que comecam o 'ahp'
#     csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f.startswith('ahp')]
#
#     if request.method == 'POST':
#         selected_dataset = request.form.get('dataset')
#         selected_alternatives_column = request.form.get('alternatives_column')
#
#         if not selected_dataset or not selected_alternatives_column:
#             flash('Please select a dataset and an alternatives column.', 'warning')
#             return redirect(url_for('main.ahp_dataset_selection'))
#
#         # guarda str na sessao dataset no app config. nao usar pq estah armazenando, abaixo.
#         current_app.config['DATA_FILE'] = os.path.join(data_dir, selected_dataset)
#
#         # guarda na sessao str dataset
#         session['ahp_selected_dataset'] = selected_dataset
#
#         # guarda na sessao str de coluna de alternativas
#         session['ahp_alternatives_column'] = selected_alternatives_column
#
#         return redirect(url_for('main.ahp_criterion_alternatives'))
#
#     return render_template('ahp/ahp_1b_datasets.html', csv_files=csv_files)
#
#     # return render_template('index.html')


@main.route('/test')
def test():
    # Example data
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'Score': [85, 90, 95, 80]
    }

    # Convert the data to a Pandas DataFrame
    df = pd.DataFrame(data)

    # Generate a graph (bar chart of scores)
    plt.figure(figsize=(6, 4))
    plt.bar(df['Name'], df['Score'], color='blue')
    plt.title('Scores by Name')
    plt.xlabel('Name')
    plt.ylabel('Score')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    img.close()

    # Pass the DataFrame and graph to the template
    return render_template('ranking.html', tables=[df.to_html(classes='table table-striped')], graph_url=graph_url)

# @main.route('/')
# def index():
#     dataset = 'ahp_cars.csv' # estah hardcoded mas pode tanto deixar ou fazer uma selecao dos datasets existentes no path
#
#     data_dir = os.path.join(current_app.root_path, '../data')
#     csv_file_path = os.path.join(data_dir, dataset)
#
#     # csv_file_path = current_app.config.get('DATA_FILE', 'ahp_cars.csv')
#     print('**** 1 >>>> csv_file_path (', type(csv_file_path), '): ', csv_file_path)
#     df = pd.read_csv(csv_file_path)
#
#     # converte dataframe em uma lista de dict
#     cars = df.to_dict(orient='records')
#
#     return render_template('index.html',
#                            cars=cars,
#                            date_time=get_timestamp(),
#                            )
