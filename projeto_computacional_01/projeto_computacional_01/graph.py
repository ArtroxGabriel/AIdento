class Graph:
    """
    Classe para abstrair as operações em grafos
    """
    def __init__(self, adj_matrix: list[list[float]]) -> None:
        """
        Inicializador que recebe uma matriz de adjacências
        """
        self.data = adj_matrix.copy()
        self.N = len(adj_matrix)

    
    def get_at(self, r_index: int, c_index: int) -> float:
        return self.data[r_index][c_index]

    
    def set_at(self, r_index: int, c_index: int, value: float) -> None:
        self.data[r_index][c_index] = value


    def get_neighbours(self, index: int) -> list[float]:
        """
        Método para acessar a distância para as cidades a partir de uma origem, dada pelo índice
        """
        return self.data[index]
    

    def get_path_cost(self, path: list[float]) -> float:
        """
        Método para dizer o custo total de um trajeto no grafo
        """
        cost = 0
        
        for index in range(self.N - 1):
            current = path[index]
            prox = path[index + 1]
            cost += self.get_at(current, prox)

        return cost

