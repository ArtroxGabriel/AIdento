from graph import Graph

class AntColony:
    def __init__(self, graph: Graph, alpha: int = 2, beta: int = 2) -> None:
        self.graph = graph
        self.ants = [i for i in range(graph.get_n())]
        self.alpha = alpha
        self.beta = beta
        self.pheromone_matrix = self.__generate_pheromone(self.graph.get_n())


    def __generate_pheromone(self, size: int) -> list[list[int]]:
        """
        Método auxiliar para inicializar a matriz de feromônios
        """
        pheromone_matrix = [[1 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            pheromone_matrix[i][i] = 0
        return pheromone_matrix
    

    def __generate_visited_matrix(self, size: int) -> list[list[int]]:
        pheromone_matrix = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            pheromone_matrix[i][i] = 1
        return pheromone_matrix


    def __get_travel_probability(self, origin: int) -> list[float]:
        denominator = sum([self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta 
                           for i in range(self.graph.get_n())])
        
        return [(self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta) / denominator 
                for i in range(self.graph.get_n())]


    def fit_inside_loop(self):
        ants_path = list()
        self.visited_matrix = self.__generate_visited_matrix(self.graph.get_n())

        for idx, ant in enumerate(self.ants):
            current_ant_path = [self.ants[idx]]
            previous_max_prob = ant

            while sum(self.visited_matrix[idx]) < self.graph.get_n():
                travel_probabilities = self.__get_travel_probability(ant)
                max_prob = max(travel_probabilities)
                idx_max_prob = travel_probabilities.index(max_prob)

                while self.visited_matrix[idx][idx_max_prob]:
                    travel_probabilities[idx_max_prob] = 0
                    max_prob = max(travel_probabilities)
                    idx_max_prob = travel_probabilities.index(max_prob)
                
                self.pheromone_matrix[previous_max_prob][idx_max_prob] += 1
                previous_max_prob = idx_max_prob

                current_ant_path.append(idx_max_prob)
                self.visited_matrix[ant][idx_max_prob] = 1
            
            ants_path.append(current_ant_path.copy())
        
        return ants_path


    def fit(self, max_epochs: int = 10):
        for _ in range(max_epochs):
            paths = self.fit_inside_loop()
            costs = [self.graph.get_path_cost(path) for path in paths]
    
        min_cost = min(costs)
        min_cost_idx = costs.index(min_cost)
        return paths[min_cost_idx]
