from random import shuffle, random, sample
from graph import Graph


class GeneticAlgorithm:
    def __init__(self, graph: Graph, pop_size: int = 100, mut_rate: float = 0.5, cross_rate: float = 0.5) -> None:
        self.graph = graph
        self.num_cities = self.graph.get_n()
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.cross_rate = cross_rate
        self.population = [self.__make_agent() for _ in range(self.pop_size)]


    def __make_agent(self):
        """
        Método para criar um agente
        """
        agent = list(range(self.num_cities))
        shuffle(agent)
        return agent


    def __fitness(self, agent):
        """
        Método para computar o valor fitness de um agente
        """
        dist = self.graph.get_path_cost(agent)
        return 1.0 / dist


    def __selection(self, k=5):
        """
        Método para escolher os agentes a serem propagados
        """
        selected = sample(self.population, k)
        selected.sort(key=lambda ind: self.graph.get_path_cost(ind))
        return selected[0]


    def __crossover(self, parent1, parent2):
        """
        Método para realizar o crossover de dois agentes
        """
        size = len(parent1)
        
        p1, p2 = sample(range(size), 2)
        start, end = min(p1, p2), max(p1, p2)
        
        child = [None] * size
        
        child[start:end+1] = parent1[start:end+1]
        
        pos = (end + 1) % size
        for city in parent2:
            if city not in child:
                child[pos] = city
                pos = (pos + 1) % size
        return child


    def __mutation(self, agent):
        """
        Método para gerar a mutação de um agente
        """
        if random() < self.mut_rate:
            i1, i2 = sample(range(len(agent)), 2)
            agent[i1], agent[i2] = agent[i2], agent[i1]
        return agent


    def fit(self, max_epochs: int = 100):
        """
        Método para rodar o algoritmo
        """
        best_agent = None
        best_distance = float('inf')
        
        for gen in range(max_epochs):
            new_population = []
            
            self.population.sort(key=lambda ind: self.graph.get_path_cost(ind))
            current_best_distance = self.graph.get_path_cost(self.population[0])
            if current_best_distance < best_distance:
                best_distance = current_best_distance
                best_agent = self.population[0][:]
            
            new_population.append(best_agent)
            
            while len(new_population) < self.pop_size:
                parent1 = self.__selection()
                parent2 = self.__selection()
                
                if random() < self.cross_rate:
                    child = self.__crossover(parent1, parent2)
                else:
                    child = parent1[:]
                
                child = self.__mutation(child)
                new_population.append(child)
            
            self.population = new_population
        
        best_agent.append(best_agent[0])

        return best_agent

