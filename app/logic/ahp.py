# coding=UTF-8
import numpy as np
import json
from operator import itemgetter

# BIBLIOGRAFIA USADA:
# Artigo original de Saaty criando o AHP, tem os calculos originais completos:
# https://doi.org/10.1016/0022-2496(77)90033-5
#
# Artigo posterior de Saaty sobre a implementação do AHP:
# https://doi.org/10.1016/0377-2217(90)90057-I
#
# Tese com explicação dos calculos do AHP e o indice aleatorio (tudo no capítulo 3).
# tem os calculos simplificados.
# https://web.tecgraf.puc-rio.br/press/publication/RosaSilva2007/RosaeSilva2007.pdf
#
# Artigo com explicação do indice aleatorio:
# https://doi.org/10.1016/0895-7177(91)90098-R

# TODO: (opcional porque estas validações também podem ser feitas no frontend)
#  1. verificações de valores nas matrizes, para garantir que estão dentro dos aceitaveis no AHP (0 a 9).
#  2. verificar as matrizes seguem a norma de formato das pairwise matrices:
#     diagonais tudo 1s, e se (X/1)ij = (1/X)ji
#  3. verificar se as matrizes de comparacao par a par (pairwise_matrices) são n x n.

'''
Classe que representa método AHP.

Attributes
----------
- process: string, nome do processo/metodo de calculo usado para o calcular os eigenvectors (auto-vectores),
           escolher entre 'eigenvalue', 'geometric', 'approximation'.
           O metodo de calculo ensinado nos slides de aula eh o 'approximation'.
- precision: integer, grau de precisão do valor. a quantidade de casas decimais exibido nos resultados.
- alternatives: lista de string, as alternativas de escolha no AHP. 
                No trabalho as alternativas são os modelos de carro.
- criterion: lista de string, criterios da escolha, os features no dataset.
- subCriterion: dict, subopcoes dos criterios. opcional, enviar {} para ter subcriterios nulo.
              útil quando o feature é discreto, os valores discretos de 
              um feature (criterio) são entendidos como subcriterios, ou
              quando é um criterio que é um agrupamento de critérios
- pairwise_matrices: dict. São as matrizes com pesos de preferencias para cada criterio ou 
                     subcriterio, com as comparações pares a pares por criterio/subcriterio.
- log: bool, se true faz prints mais detalhados dos valores.
'''


class AHP(object):

    def __init__(self, alternatives: list[str], pairwise_matrices: dict, criterion: list[str],
                 sub_criterion: dict = {}, process: str = 'eigenvalue',
                 precision: int = 4,
                 log: bool = False, return_logs: bool = True):
        self.process = process
        self.precision = precision
        self.alternatives = alternatives
        self.criterion = criterion
        self.sub_criterion = sub_criterion
        self.pairwise_matrices = pairwise_matrices
        self.log = log
        self.return_logs = return_logs

        self.logs_dict = {}

        # pesos que representam a importancia global de cada alternativa,
        # ao que diz respeito ao objetivo principal da tomada de decisão
        self.global_priorities = []
        self.total_priorities = []

    '''
    Retorna o eigenvector de valores calculado pelo modo de Aproximação de eigenvectors.

    Parameters
    ----------
    matrix: array de int, matriz a calcular o eigenvector de valores
    precision: integer, quantidade de casas decimais exibido nos resultados
    '''

    # @staticmethod
    def approximation(self, matrix: list[int], precision: int = 3):
        self.logs_dict['approximation'] = self.logs_dict.get('approximation', {})

        # 1. soma das colunas da matriz
        columns_sum = matrix.sum(axis=0)  # axis 0 considera colunas

        # 2. normalizacao dos valores das colunas
        normalized_matrix = np.divide(matrix, columns_sum)

        # 3. média das linhas da matriz, que por sí só são o eigenvector desejado
        mean_rows = normalized_matrix.mean(axis=1)  # axis 1 considera linhas

        return mean_rows.round(precision)

    '''
    Retorna o eigenvector com valores calculados pelas Médias Geometricas.

    Parametros
    ----------
    matrix: array de int, matriz a calcular o eigenvector de valores
    precision: integer, quantidade de casas decimais exibido nos resultados
    '''

    # @staticmethod
    def geometric(self, matrix: list[int], precision: int = 3):
        self.logs_dict['geometric'] = self.logs_dict.get('geometric', {})

        # 1. produto das linhas da matriz, elevado a 1/n (n=quantidade de linhas),
        # para cada linha da matriz
        geometric_mean = [np.prod(row) ** (1 / len(row)) for row in matrix]

        # 2. normalizacao dos valores (cada número / pela soma deles)
        normalized_geometric_mean = geometric_mean / sum(geometric_mean)

        return normalized_geometric_mean.round(precision)

    ''' 
    Retorna o eigenvector de valores calculado pelo modo Eigenvalue (auto-valor).
    Este modo de calculo foi criado pelo Saaty quando criou o AHP, portanto
    é preferido para utilização no método AHP.

    Parameters
    ----------
    matrix: array de int, matriz a calcular o eigenvector de valores
    precision: integer, quantidade de casas decimais exibido nos resultados
    iteraction: integer, quantidade de vezes que a recursao aconteceu
    previous_eigenvector=None, porque na primeira vez que corre é nulo
    '''

    # @staticmethod
    def eigenvalue(self, matrix: list[int], precision: int = 3,
                   iteration: int = 100, previous_eigenvector=None):
        self.logs_dict['eigenvalue'] = self.logs_dict.get('eigenvalue', {})

        # 1. elevar matriz ao quadrado
        squared_matrix = np.linalg.matrix_power(matrix, 2)

        # 2. soma das linhas e soma de colunas, axis=1 = linhas
        rows_sum = np.sum(squared_matrix, axis=1)

        #    soma das colunas apartir da soma das linhas, axis=0 = colunas
        cols_sum = np.sum(rows_sum, axis=0)

        #    normalização, o primeiro eigenvector gerado, que vai
        #    ser usado para comparar com o eigenvector anterior
        current_eigenvector = np.divide(rows_sum, cols_sum)

        # 3. fazer recursão até que a diferença entre o penúltimo eigenvector
        #    e o último eigenvector seja 0,
        #    ou até que o número de iterações seja atingido
        if previous_eigenvector is None:
            previous_eigenvector = np.zeros(matrix.shape[0])

        #    subtrai o vetor anterior do vetor atual
        difference_eigenvectors = np.subtract(current_eigenvector, previous_eigenvector).round(precision)

        if not np.any(difference_eigenvectors):
            return current_eigenvector.round(precision)

        #    recursao até que os dois eigenvectors sejam iguais, ou até que o número de interações acabe
        iteration -= 1
        if iteration > 0:
            return self.eigenvalue(squared_matrix, precision, iteration, current_eigenvector)
        else:
            return current_eigenvector.round(precision)

    ''' 
    Faz a análise da consistencia da matriz.
    Para isso calcula o "lambda max" (medida de consistencia), CI e o CR.
    Eles medem a consistência entre os critérios.

    Parameters
    ----------
    matrix : array
    '''

    @staticmethod
    def consistency(matrix):

        # a matrix deve ser maior do que 2x2 para realizar o calculo de consistencia
        if matrix.shape[0] and matrix.shape[1] > 2:

            # calcula o "lambda max", eigenvalue da matriz
            # informação nos links no topo do codigo
            lambda_max = np.real(np.linalg.eigvals(matrix).max())

            # ci = indice de consistencia, formula no links (e nos slides de aula)
            # (lambdamax - tamanho da matriz), dividido pelo tamanhho da matriz - 1
            ci = (lambda_max - len(matrix)) / (len(matrix) - 1)

            # ri = "random index", indice aleatorio, que é proposto por Saaty (criador do metodo AHP)
            # há link com explicações sobre isso no topo do codigo, e informação nos slides da aula
            ri = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45,
                  10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59}

            # cr = "consistency ratio", razao de consistencia.
            # o cr mede a consistencia das comparações par a par.
            # formula nos link, cr é o ci dividido pelo indice aleatorio, também foi dada nos slides
            cr = ci / ri[len(matrix)]

        else:
            # se matriz não for maior do que 2x2
            lambda_max = 0
            ci = 0
            cr = 0

        # o valor do cr que a funcao retorna tem que estar
        # abaixo de 0.10 (=10%) para a matriz ser consistente
        return lambda_max, ci, cr

    ''' 
    Calcula os vetores de prioridades locais.
        Eles representam os pesos/importancia comparativamente dos elementos 
        (criterios, subcriterios e alternatives), fazendo o ranking destes com base nas
        matrizes de comparação par a par.
    '''

    def local_priorities_vector(self):
        local_priorities_vectors = {}

        for criteria in self.pairwise_matrices:
            matrix = np.array(self.pairwise_matrices[criteria])

            # DEBUG
            # print(">>> /models/ahp.AHP.local_priorities_vector(...): \n1. Matrix for {criteria}:\n", matrix)

            if self.process == 'approximation':
                local_process = 'approximation'
                local_priorities = self.approximation(matrix, self.precision)
            elif self.process == 'geometric':
                local_process = 'geometric'
                local_priorities = self.geometric(matrix, self.precision)
            elif matrix.shape[0] and matrix.shape[1] >= 2:
                local_process = 'eigenvalue'
                local_priorities = self.eigenvalue(matrix, self.precision)
            else:
                local_process = 'approximation'
                local_priorities = self.approximation(matrix, self.precision)

            local_priorities_vectors[criteria] = local_priorities

            lambda_max, ci, cr = self.consistency(matrix)

            # print(">>> ahp.consistency.matrix", matrix)
            # print(">>> ahp.consistency.cr", cr)

            # <-- logs dos calculos ---
            self.logs_dict[local_process][criteria] = {
                'Local Priorities': {
                    # Local Priorities values
                    ('Preferences Vector (Averages Per Alternatives Per Criteria)'
                     if criteria != 'criterion'
                     else 'Preferences Vector (Criterion Weight)'
                    ): local_priorities.tolist(),  # JSON compatibility

                    # 'Preferences Vector\'s Averages': local_priorities.tolist(),  # Convert ndarray to list for JSON compatibility

                    # Esta soma das local_priorities sempre deve ser 1.
                    # Se o número for muito diferente de 1, isso indica que há problema nos métodos que calculam o eigenvector.
                    # Quando a soma não chega a 1 mas é próximo, o resultado está correto mas a diferença de valores
                    # é por conta do arredondamento.
                    'Sum of Local Priorities': np.round(np.sum(local_priorities), self.precision),

                    'Lambda Max': round(lambda_max, self.precision),
                    'Consistency Index': round(ci, self.precision),
                    'Consistency Ratio': round(cr, self.precision),

                    # valores da soma das prioridades locais podem
                    # variar por aprox. 0.05 por conta dos arredondamentos,
                    # mas eles devem ser bastante proximos de 1.0
                    'Assessment of correctness of calculation': (
                        'Sum of local priorities is 1.0, it shows calculations are correct.'
                        if np.sum(local_priorities) == 1
                        else 'Sum of local priorities shows calculations are correct. Slight difference from 1.0 is due to rounding numbers.'
                        if 0.96 <= np.sum(local_priorities) <= 1.05
                        else 'Sum of local priorities shows calculations are incorrect. Sum should be 1.0.'
                    ),

                    # julgamentos escolhidos sao consistentes se matriz tem
                    # cr <= 10%
                    'Assessment of consistency of matrix': (
                        'Judgements have a satisfatory consistency. Degree of consistency is under 10%.'
                        if cr <= 0.1
                        else 'Judgements do not have a satisfactory consistency. Degree of consistency is higher than 10%.'
                    )
                }
            }
            # --- logs do calculos -->

        # if self.log:
        #     json_logs = {
        #         key: (value.tolist() if isinstance(value, np.ndarray) else value)
        #         for key, value in self.logs_dict.items()
        #     }
        #     print(json.dumps(json_logs, indent=4))

        return local_priorities_vectors

    ''' 
    Calcula os vetores de prioridades globais.
        Eles representam os pesos/importancia comparativamente dos elementos 
        (criterios, subcriterios e alternatives), fazendo o ranking destes com base nas
        matrizes de comparação par a par.
    '''

    def global_priorities_vector(self, priorities, weights, criterion):
        for criteria in criterion:
            peso = weights[criterion.index(criteria)]
            local_priorities = priorities[criteria]
            global_priorities = np.round(peso * local_priorities, self.precision)

            # recursao, caso o criterio contenha subcriterios
            if criteria in self.sub_criterion:
                self.global_priorities_vector(priorities, global_priorities, self.sub_criterion[criteria])
            else:
                self.global_priorities.append(global_priorities)

                # <-- logs dos calculos ---
                self.logs_dict[self.process][criteria]['Global Priorities'] = (
                    self.logs_dict[self.process][criteria].get('Global Priorities', {})
                )
                self.logs_dict[self.process][criteria]['Global Priorities'] = {
                    'Global Priorities values': global_priorities.tolist(),
                    'Sum of Global Priorities': sum(global_priorities).round(self.precision)
                }
                # --- logs do calculos -->

    '''
    Retorna dict com os valores de ranking finais, calculados no 
    modo escolhido na chamada da função (geometric, eigenvalue, approximation)

    Parameters
    ----------
    ordered: str. 'no', 'desc', 'asc'.
             se 'no', retorna vetor desordenado.
             se 'desc' retorna vetor ordenado do maior para o menor (decrescente).
             se 'asc', 'yes' ou qq outro valor, 
                retorna vetor ordenado do menor para o maior (ascendente).
    '''

    def final_rank(self, ordered: str = 'no'):
        priorities = self.local_priorities_vector()
        self.global_priorities_vector(priorities, priorities['criterion'], self.criterion)
        priorities = np.array(self.global_priorities)
        priorities = priorities.sum(axis=0).round(self.precision)

        # ranking = {}
        ranking = dict(zip(self.alternatives, priorities))
        if ordered != 'no':
            reverse = False
            if ordered == 'desc':
                reverse = True
            ranking = dict(sorted(ranking.items(), key=itemgetter(1), reverse=reverse))

        # DEBUG
        # print(">>> /models/ahp.AHP.final_rank(...): 1. Final Priorities", priorities)
        # print(">>> /models/ahp.AHP.final_rank(...): 2. Ranking", ranking)

        if self.log:
            json_logs = {
                key: (value.tolist() if isinstance(value, np.ndarray) else value)
                for key, value in self.logs_dict.items()
            }
            # print(json.dumps(json_logs, indent=4))

        if self.return_logs:
            return ranking, self.logs_dict
        else:
            return ranking, {}


'''
Teste dos metodos: 
- Retirar comentários e correr somente este ficheiro.
- Verificar se os valores de razao consistencia estão abaixo de 10%
'''
# if __name__ == '__main__':
#     matriz = np.array([
#         [1, 5, 3],
#         [1 / 5, 1, 1 / 4],
#         [1 / 3, 4, 1]
#     ])
#     precision = 2
#
#     print('Calculo por aproximação: ', AHP.approximation(matriz, precision))
#     print('Calculo por média geometrica: ', AHP.geometric(matriz, precision))
#     print('Calculo por Eigenvalue (auto-valor): ', AHP.eigenvalue(matriz, precision))
#     print('Consistencia da matriz: ', AHP.consistency(matriz))
