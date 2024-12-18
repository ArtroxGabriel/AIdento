from graph import Graph


class AntColony:
    def __init__(
        self,
        graph: Graph,
        alpha: int = 2,
        beta: int = 2,
        ro: float = 0.5,
        Q: float = 5
    ) -> None:
        self.graph = graph
        self.ants = [i for i in range(graph.get_n())]
        self.alpha = alpha
        self.beta = beta
        self.pheromone_matrix = self.__generate_pheromone(self.graph.get_n())
        self.ro = ro
        self.Q = Q


    def __generate_pheromone(self, size: int) -> list[list[int]]:
        """
        Auxiliary method to initialize the pheromone matrix
        """
        pheromone_matrix = [[1 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            pheromone_matrix[i][i] = 0
        return pheromone_matrix
    

    def __generate_visited_matrix(self, size: int) -> list[list[int]]:
        """
        Auxiliary method to initialize the visited matrix
        """
        visited_matrix = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            visited_matrix[i][i] = 1
        return visited_matrix


    def __get_travel_probability(self, origin: int) -> list[float]:
        """
        Auxiliary method to compute travel probabilities
        """
        denominator = sum([self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta 
                           for i in range(self.graph.get_n())])
        
        return [(self.pheromone_matrix[origin][i]**self.alpha * (1/self.graph.get_at(origin, i, safe=True))**self.beta) / denominator 
                for i in range(self.graph.get_n())]


    def __update_pheromone_matrix(self, ant: int, distance: int, origin: int, destination: int) -> None:
        """
        Auxiliary method to update the pheromone matrix
        """
        # Evaporation
        self.pheromone_matrix[origin][destination] *= (1 - self.ro)

        # Addition
        self.pheromone_matrix[origin][destination] += (self.Q)/(distance)


    def fit_inside_loop(self):
        """
        Internal loop of the ant colony
        """
        ants_path = list()  # Initialize the paths (a matrix)
        self.visited_matrix = self.__generate_visited_matrix(self.graph.get_n())  # Matrix indicating visited vertices

        for idx, initial_pos in enumerate(self.ants):  # For each ant
            current_ant_path = [initial_pos]  # Initialize its path
            current_pos = initial_pos
            distance = 0  # Initialize its distance

            while sum(self.visited_matrix[idx]) < self.graph.get_n():  # While it hasn't visited all nodes
                travel_probabilities = self.__get_travel_probability(current_pos)  # Calculate the probabilities
                max_prob = max(travel_probabilities)  # Take the maximum
                next_pos = travel_probabilities.index(max_prob)  # Index of the maximum

                # While the maximum is not a new vertex
                while self.visited_matrix[idx][next_pos]:
                    travel_probabilities[next_pos] = 0
                    max_prob = max(travel_probabilities)
                    next_pos = travel_probabilities.index(max_prob)
                
                distance += self.graph.get_at(current_pos, next_pos)  # Update the path

                self.__update_pheromone_matrix(idx, distance, current_pos, next_pos)  # Update the pheromones
                current_pos = next_pos  # Update the ant's current position

                current_ant_path.append(next_pos)  # Add the position to be visited to the path
                self.visited_matrix[idx][next_pos] = 1  # Mark that it has been visited
            
            ants_path.append(current_ant_path.copy())
        
        return ants_path


    def fit(self, max_epochs: int = 10):
        """
        External loop of the ant colony
        """
        for _ in range(max_epochs):
            paths = self.fit_inside_loop()
            costs = [self.graph.get_path_cost(path) for path in paths]
    
        min_cost = min(costs)
        min_cost_idx = costs.index(min_cost)
        return paths[min_cost_idx]
