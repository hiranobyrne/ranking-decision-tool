from flask import flash, render_template, request, current_app, redirect, url_for, session
import csv
import json
import os
import pandas as pd
from fractions import Fraction
from app.routes import main
from app.logic import AHP
from app.utils.utils import get_timestamp, load_csv

# print(">>> Loading: ahp_routes.py")


# Route anterior ao comeco do metodo AHP. Faz:
# - O dataset está pre-selecionado, pede-se confirmacao para continuar
# - Há botão no canto da tela para ir para o dataset de teste
@main.route('/ahp', methods=['GET', 'POST'])
def ahp_confirm_dataset():
    # print(">>> ahp_dataset_selection()")

    dataset_name = 'ahp_aprendizagem_automatica_cars.csv'
    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets', dataset_name)

    selected_alternatives_column = 'Brand_Model'

    if request.method == 'POST':
        session['ahp_selected_dataset'] = dataset_name
        session['ahp_alternatives_column'] = selected_alternatives_column

        return redirect(url_for('main.ahp_criterion_alternatives'))

    return render_template('ahp/ahp_1a_confirm_dataset.html',
                           csv_files=[dataset_name],
                           alternatives_column=selected_alternatives_column)


# Route com os datasets de teste
# - Permite selecao de qq dataset comecando com 'ahp_'
# - Permite selecao de coluna de alternativas
@main.route('/')
@main.route('/ahp/select_dataset', methods=['GET', 'POST'])
def ahp_dataset_selection():
    # print(">>> ahp_dataset_selection()")

    # busca o path dos dados que estah em config.py
    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')

    # print(">>> ahp_dataset_selection.data_dir:", data_dir)

    # busca todos csv na diretoria dos dados que comecam o 'ahp'
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and f.startswith('ahp')]

    if request.method == 'POST':
        selected_dataset = request.form.get('dataset')
        selected_alternatives_column = request.form.get('alternatives_column')

        if not selected_dataset or not selected_alternatives_column:
            flash('Please select a dataset and an alternatives column.', 'warning')
            return redirect(url_for('main.ahp_dataset_selection'))

        # guarda str na sessao dataset no app config. nao usar pq estah armazenando, abaixo.
        current_app.config['DATA_FILE'] = os.path.join(data_dir, selected_dataset)

        # guarda na sessao str dataset
        session['ahp_selected_dataset'] = selected_dataset

        # guarda na sessao str de coluna de alternativas
        session['ahp_alternatives_column'] = selected_alternatives_column

        return redirect(url_for('main.ahp_criterion_alternatives'))

    return render_template('ahp/ahp_1b_datasets.html', csv_files=csv_files)


@main.route('/load_columns', methods=['GET'])
def load_columns():
    # print(">>> load_columns()")

    # precisa ser request.args.get ao inves de variavel de sessao pq
    # a variavel de sessao ainda nao foi gravada
    dataset = request.args.get('dataset')
    if not dataset:
        return json.dumps([])

    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
    csv_file_path = os.path.join(data_dir, dataset)

    try:
        df = pd.read_csv(csv_file_path)
        columns = df.columns.tolist()
        return json.dumps(columns)
    except Exception as e:
        return json.dumps([])


# Route inicial do AHP, apos o dataset ter sido selecionado na tela anterior:
# 1. Selecao das alternativas (modelos de carro) que deseja-se fazer a comparacao par a par;
# 2. Selecao dos criterios de comparacao (features / colunas do csv).
@main.route('/ahp/criterion_alternatives', methods=['GET', 'POST'])
def ahp_criterion_alternatives():
    # print(">>> ahp_criterion_alternatives()")

    # busca variaveis de sessao
    selected_dataset = session.get('ahp_selected_dataset')
    alternatives_column = session.get('ahp_alternatives_column')

    # print(">>> ahp_criterion_alternatives.selected_dataset:", selected_dataset)
    # print(">>> ahp_criterion_alternatives.alternatives_column:", alternatives_column)

    # se coluna com as alternativas estiver faltando, redireciona para escolha de dataset (tela 1)
    if not selected_dataset or not alternatives_column:
        flash('Please select a dataset and alternatives column first.', 'warning')
        return redirect(url_for('main.ahp_dataset_selection'))

    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
    csv_file_path = os.path.join(data_dir, selected_dataset)

    dataset = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        # nomes das colunas (criterios/features)
        columns = reader.fieldnames
        for row in reader:
            dataset.append(row)

        # se o dataset usado for o dataset padrao,
        # adiciona as colunas usadas no link do /car_versions
        if selected_dataset.endswith('aprendizagem_automatica_cars.csv'):
            columns = ['Fuel_Consumption_Combined',
                       'CO2_Emissions_Combined',
                       'Net_Maximum_Power',
                       'Catalog_Price',
                       'Number_of_Seats',
                       'Curb_Weight',
                       'Maximum_Allowed_Vehicle_Mass',
                       # 'Breakdowns_Per_Car',
                       'Date_of_First_Registration']

    # guarda os valores da coluna de alternativas
    alternatives = [row[alternatives_column] for row in dataset if alternatives_column in row]

    # print(">>> alternatives", alternatives)

    unique_alternatives = list(dict.fromkeys(alternatives))

    # print(">>> unique_alternatives", unique_alternatives)

    if request.method == 'POST':
        selected_criterion = []
        selected_alternatives = []

        # Collect selected criterion from the form
        for key, value in request.form.items():
            if key.startswith("criterion_") and value:
                selected_criterion.append(value)
            elif key.startswith("alternative_") and value:
                selected_alternatives.append(value)

        # redirecionamento para preservar o estado dos criterion e alternativas selecionados
        return redirect(url_for('main.ahp_criterion_weights',
                                selected_criterion=','.join(selected_criterion),
                                selected_alternatives=','.join(selected_alternatives)))

    return render_template('ahp/ahp_2_criterion_alternatives.html',
                           dataset=dataset,
                           columns=columns,
                           alternatives=unique_alternatives,
                           alternatives_column=alternatives_column,
                           selected_criterion=session.get('ahp_selected_criterion', []))

# 2a. route, acedida a partir de '/ahp'. Faz:
# 1. Atribuicao de pesos para a matriz de pesos dos criterios em si.
@main.route('/ahp/criterion/weights', methods=['GET', 'POST'])
def ahp_criterion_weights():
    # print(">>> ahp_criterion_weights()")

    # set variaveis de sessao
    # deixa aqui, se por na route anterior dah erro
    session['ahp_selected_criterion'] = request.args.get('selected_criterion', '').split(',')
    session['ahp_selected_alternatives'] = request.args.get('selected_alternatives', '').split(',')

    # busca variaveis de sessao
    selected_dataset = session.get('ahp_selected_dataset')
    alternatives_column = session.get('ahp_alternatives_column')
    selected_criterion = session.get('ahp_selected_criterion', [])

    if not selected_dataset or not alternatives_column:
        flash('Please select a dataset and alternatives column first.', 'warning')
        return redirect(url_for('main.ahp_dataset_selection'))

    # print (">>> ahp_criterion_weights().selected_criterion", selected_criterion)
    num_criteria = len(selected_criterion)
    indexed_cols = list(enumerate(selected_criterion))

    if request.method == 'POST':
        pairwise_matrices = {}
        criterion_matrix = []
        for i in range(num_criteria):
            row = []
            for j in range(num_criteria):
                if i == j:
                    row.append(1)
                else:
                    key = f"criterion-matrix-{i}-{j}"
                    value = request.form.get(key, '1')
                    try:
                        row.append(float(Fraction(value)))
                    except ValueError:
                        row.append(1)
            criterion_matrix.append(row)
        pairwise_matrices['criterion'] = criterion_matrix

        # guarda variavel de sessao
        session['ahp_pairwise_matrices'] = json.dumps(pairwise_matrices)

        # DEBUG
        # print(">>> ahp_criterion_weights.pairwise_matrices", pairwise_matrices)

        return redirect(url_for('main.ahp_alternatives_weights'))

    return render_template('ahp/ahp_criterion_weights.html',
                           indexed_cols=indexed_cols,
                           num_criteria=num_criteria)

# 3a. route, acedida a partir de '/ahp'. Faz:
# 1. Atribuicao de pesos para cada um dos criterios, em matrizes de comparacao par a par;
@main.route('/ahp/alternatives/weights', methods=['GET', 'POST'])
def ahp_alternatives_weights():
    # print(">>> ahp_alternatives_weights()")

    # variaveis de sessao
    selected_dataset = session.get('ahp_selected_dataset')
    alternatives_column = session.get('ahp_alternatives_column')
    selected_criterion = session.get('ahp_selected_criterion', [])
    selected_alternatives = session.get('ahp_selected_alternatives', [])

    if not selected_dataset or not alternatives_column:
        flash('Please select a dataset and alternatives column first.', 'warning')
        return redirect(url_for('main.ahp_dataset_selection'))

    num_alternatives = len(selected_alternatives)

    if request.method == 'POST':
        # busca conteudo da variaveis de sessao e
        # faz tratamento pra ler str como json
        pairwise_matrices = session.get('ahp_pairwise_matrices', "{}")
        if isinstance(pairwise_matrices, str):
            pairwise_matrices = json.loads(pairwise_matrices)

        for criteria in selected_criterion:
            matrix = []
            for i in range(num_alternatives):
                row = []
                for j in range(num_alternatives):
                    if i == j:
                        row.append(1)
                    else:
                        key = f"{criteria}-matrix-{i}-{j}"
                        value = request.form.get(key)

                        if value:
                            try:
                                row.append(float(Fraction(value)))
                            except ValueError:
                                row.append(1)
                        else:
                            row.append(1)

                matrix.append(row)
            pairwise_matrices[criteria] = matrix

        # guardar variaveis de sessao
        session['ahp_pairwise_matrices'] = json.dumps(pairwise_matrices)

        return redirect(url_for('main.ahp_ranking'))

    return render_template('ahp/ahp_alternatives_weights.html',
                           selected_criterion=selected_criterion,
                           selected_alternatives=selected_alternatives,
                           num_alternatives=num_alternatives)



# # Segunda route, acedida a partir de '/ahp'. Faz:
# # 1. Atribuicao de pesos para cada um dos criterios, em matrizes de comparacao par a par;
# # 2. Atribuicao de pesos para a matriz de pesos dos criterios em si.
# @main.route('/ahp/matrices', methods=['GET', 'POST'])
# def ahp_matrices():
#     print(">>> ahp_matrices()")
#
#     selected_dataset = session.get('selected_dataset')
#     alternatives_column = session.get('alternatives_column')
#
#     # se coluna com as alternativas estiver faltando, redireciona para escolha de dataset (tela 1)
#     if not selected_dataset or not alternatives_column:
#         flash('Please select a dataset and alternatives column first.', 'warning')
#         return redirect(url_for('main.ahp_dataset_selection'))
#
#     data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
#
#     # nao eh usado, mas mantive para futuramente exibir o path do dataset na pagina
#     csv_file_path = os.path.join(data_dir, selected_dataset)
#
#     # popula selected_criterion e selected_alternatives query parameters
#     selected_criterion = request.args.get('selected_criterion', '').split(',')
#     selected_alternatives = request.args.get('selected_alternatives', '').split(',')
#
#     # DEBUG
#     # print(f">>>> ahp_matrices.selected_criterion:", selected_criterion)
#     # print(f">>>> ahp_matrices.selected_alternatives:", selected_alternatives)
#
#     num_alternatives = len(selected_alternatives)
#
#     # preprocessa os indexes para nao dar erro de enumerate no Jinja
#     indexed_cols = list(enumerate(selected_criterion))
#
#     # DEBUG
#     # print(f">>>> ahp_matrices.indexed_cols:", indexed_cols)
#
#     if request.method == 'POST':
#         pairwise_matrices = {}
#
#         # DEBUG
#         # print(">>> form data:", request.form)
#
#         # pairwise_matrices para cada um dos criterios selecionados
#         for criteria in selected_criterion:
#             matrix = []
#             for i in range(num_alternatives):
#                 row = []
#                 for j in range(num_alternatives):
#                     if i == j:
#                         # diagonal sempre eh 1
#                         row.append(1)
#                     else:
#                         key = f"{criteria}-matrix-{i}-{j}"
#                         value = request.form.get(key)
#                         # DEBUG
#                         # print(f">>>> 1a. ahp_matrices [{criteria}][{i}][{j}]:", value)
#
#                         if value:
#                             try:
#                                 # converte para fracao e depois para float
#                                 row.append(float(Fraction(value)))
#                             except ValueError:
#                                 row.append(1)
#
#                                 # DEBUG
#                                 # print(">>>> 2b. ahp_matrices [fraction Convertion] value:", value)
#                         else:
#                             # DEBUG
#                             # print(">>>> 2c. ahp_matrices: NO VALUE FOUND!!!, row.append(1)")
#                             row.append(1)
#                 matrix.append(row)
#             pairwise_matrices[criteria] = matrix
#
#             # "criterion" pairwise_matrix
#             num_criteria = len(selected_criterion)
#             criterion_matrix = []
#             for i in range(num_criteria):
#                 row = []
#                 for j in range(num_criteria):
#                     if i == j:
#                         # diagonal sempre eh 1
#                         row.append(1)
#                     else:
#                         key = f"criterion-matrix-{i}-{j}"
#                         value = request.form.get(key, '1')
#                         # print(f">>>> 3. ahp_matrices [criterion][{i}][{j}]:", value)
#                         try:
#                             # print(">>>> 3a. ahp_matrices [value]:", value)
#                             row.append(float(Fraction(value)))
#                         except ValueError:
#                             # print(">>>> 3b. ahp_matrices [fraction Convertion] value:", value)
#                             row.append(1)
#                 criterion_matrix.append(row)
#             pairwise_matrices['criterion'] = criterion_matrix
#
#         # guarda dados de sessao
#         session['selected_criterion'] = selected_criterion
#         session['selected_alternatives'] = selected_alternatives
#         session['pairwise_matrices'] = json.dumps(pairwise_matrices)
#
#         return redirect(url_for('main.ahp_ranking'))
#
#     return render_template('ahp/ahp_3_matrices.html',
#                            indexed_cols=indexed_cols,
#                            selected_criterion=selected_criterion,
#                            selected_alternatives=selected_alternatives,
#                            num_alternatives=num_alternatives)


# Terceira e final route do AHP, acedida a partir de '/ahp/matrices'. Faz:
# 1. Exibe o rankeamento pelo AHP;
# 2. Permite a selecao do modo de calculo (geomtrico, aproximado, eigenvalue).
@main.route('/ahp/ranking', methods=['GET'])
def ahp_ranking():
    # print(">>> ahp_ranking()")

    # busca dados de sessao
    selected_criterion = session.get('ahp_selected_criterion', [])
    selected_alternatives = session.get('ahp_selected_alternatives', [])
    pairwise_matrices = json.loads(session.get('ahp_pairwise_matrices', '{}'))
    selected_dataset = session.get('ahp_selected_dataset')
    alternatives_column = session.get('ahp_alternatives_column')


    logs = {}

    # DEBUG
    # print(">>>> ahp_ranking.pairwise_matrices: ", pairwise_matrices)

    # se coluna com as alternativas estiver faltando, redireciona para escolha de dataset (tela 1)
    if not selected_dataset or not alternatives_column:
        flash('Please select a dataset and alternatives column first.', 'warning')
        return redirect(url_for('main.ahp_dataset_selection'))

    # faz o path pro dataset
    data_dir = os.path.join(current_app.root_path, '../data/csv_datasets')
    csv_file_path = os.path.join(data_dir, selected_dataset)

    # full_dataset = {}
    car_data = {}
    all_columns = []

    # Use the new utility function to load the dataset and columns
    car_data, all_columns = load_csv(csv_file_path, selected_alternatives, alternatives_column)

    # se o dataset usado for o dataset padrao,
    # adiciona as colunas usadas no link do /car_versions
    if selected_dataset.endswith('aprendizagem_automatica_cars.csv'):
        all_columns.append('Brand')
        all_columns.append('Trade_Name')

    # print(">>> ahp_ranking().car_data", car_data)

    # if all_columns:
    #     for row in full_dataset:
    #         if row[alternatives_column] in selected_alternatives:
    #             car_data[row[alternatives_column]] = row

    # car_data = {}
    # all_columns = []
    #
    # # le dados do CSV
    # with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #
    #     # busca nomes de todas colunas
    #     all_columns = reader.fieldnames
    #     for row in reader:
    #         if row[alternatives_column] in selected_alternatives:
    #             car_data[row[alternatives_column]] = row

    # query strings com os processos/metodos de calculo selecionados.
    # se nulo, o default é 'eigenvalue'
    selected_process = request.args.get('process', 'eigenvalue')

    alternatives = selected_alternatives
    criterion = selected_criterion
    log = False
    return_logs = True

    if selected_process == 'all':
        # calcula o ranking para todos process/metodos
        processes = ['eigenvalue', 'geometric', 'approximation']
        all_rankings = {}
        all_logs = {}
        for process in processes:
            ahp = AHP(process=process,
                      alternatives=alternatives,
                      pairwise_matrices=pairwise_matrices,
                      criterion=criterion,
                      log=log,
                      return_logs=return_logs)
            all_rankings[process], all_logs[process] = ahp.final_rank(ordered='desc')

        # print(">>> ahp_ranking.all_logs", all_logs)

        return render_template('ahp/ahp_4_ranking.html',
                               selected_process=selected_process,
                               all_rankings=all_rankings,
                               car_data=car_data,
                               all_columns=all_columns,
                               selected_criterion=selected_criterion,
                               alternatives_column=alternatives_column,
                               date_time=get_timestamp(),
                               pairwise_matrices=pairwise_matrices,
                               selected_alternatives=selected_alternatives,
                               logs=all_logs)
    else:
        logs = {}
        # calcula o ranking para o processo/metodo de calculo selecionado
        ahp = AHP(process=selected_process,
                  alternatives=alternatives,
                  pairwise_matrices=pairwise_matrices,
                  criterion=criterion,
                  log=log,
                  return_logs=return_logs)
        rankings, logs = ahp.final_rank(ordered='desc')

        # print(">>> ahp_ranking.logs", logs)

        # deixar apenas um return render_template
        return render_template('ahp/ahp_4_ranking.html',
                               selected_process=selected_process,
                               rankings=rankings,
                               car_data=car_data,
                               all_columns=all_columns,
                               selected_criterion=selected_criterion,
                               alternatives_column=alternatives_column,
                               date_time=get_timestamp(),
                               pairwise_matrices=pairwise_matrices,
                               selected_alternatives=selected_alternatives,
                               logs=logs)
