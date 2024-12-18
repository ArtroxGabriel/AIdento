import random
from graph import Graph


class Genetic:
    def __init__(
        self,
        graph: Graph,
        population_size: int = 300,
        crossover_rate: float = 0.5,
        mutation_rate: float = 0.2,
        num_generations: int = 500,
    ) -> None:
        self.graph = graph
        self.num_cities = self.graph.get_n()
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.population = self.__initial_population()


    def __create_individual(self):
        '''
        Auxiliary method to initialize an individual
        as a random permutation of city indices
        '''
        individual = list(range(self.num_cities))
        random.shuffle(individual)
        return individual


    def __compute_route_distance(self, individual):
        '''
        Auxiliary method to compute the total distance
        of the route represented by an individual.
        '''
        distance = 0
        for i in range(len(individual)):
            from_city = individual[i]
            to_city = individual[(i + 1) % len(individual)]
            distance += self.graph.get_at(from_city, to_city)
        return distance


    def __fitness(self, individual):
        '''
        Auxiliary method to compute the fitness of an individual based
        on the inverse of its route distance.
        '''
        dist = self.__compute_route_distance(individual)
        return 1.0 / dist


    def __initial_population(self):
        '''
        Auxiliary method to create the initial population of random individuals.
        '''
        return [self.__create_individual() for _ in range(self.population_size)]


    def __tournament_selection(self, k=3):
        '''
        Auxiliary method to randomly select k
        individuals and return the best (lowest distance)
        '''
        selected = random.sample(self.population, k)
        selected.sort(key=lambda ind: self.__compute_route_distance(ind))
        return selected[0]


    def __order_crossover(self, parent1, parent2):
        '''
        Auxiliary method implementing order crossover (OX).
        '''
        size = len(parent1)
        
        # choose two random cut points
        p1, p2 = random.sample(range(size), 2)
        start, end = min(p1, p2), max(p1, p2)
        
        child = [None] * size
        
        child[start:end+1] = parent1[start:end+1]
        
        pos = (end + 1) % size
        for city in parent2:
            if city not in child:
                child[pos] = city
                pos = (pos + 1) % size
        return child


    def __swap_mutation(self, individual):
        '''
        Auxiliary method implementing swap mutation.
        With a given mutation rate, two cities in the
        route are swapped to create variation.
        '''
        if random.random() < self.mutation_rate:
            i1, i2 = random.sample(range(len(individual)), 2)
            individual[i1], individual[i2] = individual[i2], individual[i1]
        return individual


    def genetic_algorithm_tsp(self):
        '''
        Main method that runs the genetic algorithm for a given number of generations.
        '''
        best_individual = None
        best_distance = float('inf')
        
        for gen in range(self.num_generations):
            new_population = []
            
            self.population.sort(key=lambda ind: self.__compute_route_distance(ind))
            current_best_distance = self.__compute_route_distance(self.population[0])
            if current_best_distance < best_distance:
                best_distance = current_best_distance
                best_individual = self.population[0][:]
            
            new_population.append(best_individual)
            
            while len(new_population) < self.population_size:
                parent1 = self.__tournament_selection()
                parent2 = self.__tournament_selection()
                
                # crossover
                if random.random() < self.crossover_rate:
                    child = self.__order_crossover(parent1, parent2)
                else:
                    # no crossover, just copy a parent
                    child = parent1[:]
                
                # mutation
                child = self.__swap_mutation(child)
                new_population.append(child)
            
            self.population = new_population
        
        return best_individual, best_distance
