from graph import Graph
from random import randint, choices

class AntColony:
    def __init__(self, graph: Graph, alpha: int = 2, beta: int = 2, ro: float = 0.5, Q: float = 5, num_ants: int = 100) -> None:
        self.graph = graph
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.pheromone_matrix = self.__generate_pheromone(self.graph.get_n())
        self.ro = ro
        self.Q = Q
        self.loss = []


    def __generate_pheromone(self, size: int) -> list[list[int]]:
        """
        Método auxiliar para inicializar a matriz de feromônios
        """
        pheromone_matrix = [[1 for _ in range(size)] for _ in range(size)]
        return pheromone_matrix
    

    def __generate_visited_matrix(self, size: int) -> list[list[int]]:
        """
        Método auxiliar para inicializar a matriz de visitas
        """
        visited_matrix = [[0 for _ in range(size)] for _ in range(size)]
        return visited_matrix


    def __get_travel_probability(self, origin: int) -> list[float]:
        """
        Método auxiliar para computar as probabilidades de percurso
        """
        denominator = sum([self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta 
                           for i in range(self.graph.get_n())])
        
        return [(self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta) / denominator 
                for i in range(self.graph.get_n())]


    def __evaporate_pheromone_matrix(self) -> None:
        """
        Método auxiliar para evaporar os valores antigos da matriz
        """
        n = self.graph.get_n()
        for i in range(n):
            for j in range(n):
                self.pheromone_matrix[i][j] *= (1 - self.ro)


    def __update_pheromone_matrix(self, distances: list[int], ant_paths: list[list[int]]) -> None:
        """
        Método auxiliar para atualizar a matriz de feromônios
        """

        for idx in range(self.num_ants):
            paths = ant_paths[idx]
            distance = distances[idx]
            for i in range(self.graph.get_n() - 1):
                self.pheromone_matrix[paths[i]][paths[i+1]] += (self.Q)/distance
        
        self.__evaporate_pheromone_matrix()


    def __fit_inside_loop(self):
        """
        Loop interno da colônia de formigas
        """
        ants_path = list()  # Inicializar os caminhos (uma matriz)
        ants = [randint(0, self.graph.get_n()-1) for _ in range(self.num_ants)]
        self.visited_matrix = self.__generate_visited_matrix(self.num_ants)  # Matriz que diz os vértices visitados
        distances = list()
        
        for idx, initial_pos in enumerate(ants):  # Pra cada formiga
            self.visited_matrix[idx][initial_pos] = 1
            current_ant_path = [initial_pos]  # Inicialize seu caminho
            current_pos = initial_pos
            distance = 0  # Inicialize sua distância

            while sum(self.visited_matrix[idx]) < self.graph.get_n():  # Enquanto ela não visitar todos os nós
                travel_probabilities = self.__get_travel_probability(current_pos)  # Calcule as probabilidades
                indexes = range(len(travel_probabilities))
                next_pos = choices(indexes, weights=travel_probabilities, k=1)[0]  # Pegue uma posição baseada na sua probabilidade

                # Enquanto o máximo não for um vértice novo
                while self.visited_matrix[idx][next_pos] != 0:
                    travel_probabilities[next_pos] = 0
                    next_pos = choices(indexes, weights=travel_probabilities, k=1)[0]
                
                distance += self.graph.get_at(current_pos, next_pos)  # Atualizar o caminho

                current_pos = next_pos  # Atualiza a posição atual da formiga

                current_ant_path.append(next_pos)  # Coloca a posição a ser visitada no caminho
                self.visited_matrix[idx][next_pos] = 1  # Diz que foi visitado
            
            distances.append(distance)
            current_ant_path.append(initial_pos)
            ants_path.append(current_ant_path.copy())

        # Atualização global da matriz de feromônios
        self.__update_pheromone_matrix(distances, ants_path)

        return ants_path


    def fit(self, max_epochs: int = 10):
        """
        Loop externo da colônia de formigas
        """
        for _ in range(max_epochs):
            paths = self.__fit_inside_loop()
            costs = [self.graph.get_path_cost(path) for path in paths]
            self.loss.append(min(costs))
    
        min_cost = min(costs)
        min_cost_idx = costs.index(min_cost)
        return paths[min_cost_idx]

