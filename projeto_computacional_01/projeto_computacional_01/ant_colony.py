from graph import Graph

class AntColony:
    def __init__(self, graph: Graph, alpha: int = 2, beta: int = 2, ro: float = 0.5, Q: float = 5) -> None:
        self.graph = graph
        self.ants = [i for i in range(graph.get_n())]
        self.alpha = alpha
        self.beta = beta
        self.pheromone_matrix = self.__generate_pheromone(self.graph.get_n())
        self.ro = ro
        self.Q = Q


    def __generate_pheromone(self, size: int) -> list[list[int]]:
        """
        Método auxiliar para inicializar a matriz de feromônios
        """
        pheromone_matrix = [[1 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            pheromone_matrix[i][i] = 0
        return pheromone_matrix
    

    def __generate_visited_matrix(self, size: int) -> list[list[int]]:
        """
        Método auxiliar para inicializar a matriz de visitas
        """
        visited_matrix = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            visited_matrix[i][i] = 1
        return visited_matrix


    def __get_travel_probability(self, origin: int) -> list[float]:
        """
        Método auxiliar para computar as probabilidades de percurso
        """
        denominator = sum([self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta 
                           for i in range(self.graph.get_n())])
        
        return [(self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta) / denominator 
                for i in range(self.graph.get_n())]


    def __update_pheromone_matrix(self, ant: int, distance: int, origin: int, destination: int) -> None:
        """
        Método auxiliar para atualizar a matriz de feromônios
        """
        # Evaporação
        self.pheromone_matrix[origin][destination] *= (1 - self.ro)

        # Adição
        self.pheromone_matrix[origin][destination] += (self.Q)/(distance)


    def fit_inside_loop(self):
        """
        Loop interno da colônia de formigas
        """
        ants_path = list()  # Inicializar os caminhos (uma matriz)
        self.visited_matrix = self.__generate_visited_matrix(self.graph.get_n())  # Matriz que diz os vértices visitados

        for idx, initial_pos in enumerate(self.ants):  # Pra cada formiga
            current_ant_path = [initial_pos]  # Inicialize seu caminho
            current_pos = initial_pos
            distance = 0  # Inicialize sua distância

            while sum(self.visited_matrix[idx]) < self.graph.get_n():  # Enquanto ela não visitar todos os nós
                travel_probabilities = self.__get_travel_probability(current_pos)  # Calcule as probabilidades
                max_prob = max(travel_probabilities)  # Pegue o máximo
                next_pos = travel_probabilities.index(max_prob)  # Índice do máximo

                # Enquanto o máximo não for um vértice novo
                while self.visited_matrix[idx][next_pos]:
                    travel_probabilities[next_pos] = 0
                    max_prob = max(travel_probabilities)
                    next_pos = travel_probabilities.index(max_prob)
                
                distance += self.graph.get_at(current_pos, next_pos)  # Atualizar o caminho

                self.__update_pheromone_matrix(idx, distance, current_pos, next_pos)  # Atualizar os feromônios
                current_pos = next_pos  # Atualiza a posição atual da formiga

                current_ant_path.append(next_pos)  # Coloca a posição a ser visitada no caminho
                self.visited_matrix[idx][next_pos] = 1  # Diz que foi visitado
            
            ants_path.append(current_ant_path.copy())
        
        return ants_path


    def fit(self, max_epochs: int = 10):
        """
        Loop externo da colônia de formigas
        """
        for _ in range(max_epochs):
            paths = self.fit_inside_loop()
            costs = [self.graph.get_path_cost(path) for path in paths]
    
        min_cost = min(costs)
        min_cost_idx = costs.index(min_cost)
        return paths[min_cost_idx]

