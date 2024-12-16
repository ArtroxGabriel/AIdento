class Graph:
    """
    Classe para abstrair as operações em grafos
    """
    def __init__(self, adj_matrix: list[list[float]]) -> None:
        """
        Inicializador que recebe uma matriz de adjacências
        """

        try:
            assert type(adj_matrix) == list
        except AssertionError:
            raise TypeError("Isso daí num é matriz não, dotô. Matriz é lista de listas")
        
        try:
            n = len(adj_matrix)
            for l in adj_matrix:
                c = len(l)
                assert n == c
        except TypeError:
            raise TypeError("Isso daí num é matriz não, dotô. Matriz é lista de listas")
        except AssertionError:
            raise TypeError("Uma matriz de adjacências PRECISA ser quadrada, dotô")
        
        self.data = adj_matrix
        self.N = len(adj_matrix)

    
    def get_at(self, r_index: int, c_index: int) -> float:
        try:
            assert 0 <= r_index <= self.N
            assert 0 <= c_index <= self.N
        except AssertionError:
            raise IndexError("Índice fora do intervalo, dotô")
        
        return self.data[r_index][c_index]

    
    def set_at(self, r_index: int, c_index: int, value: float) -> None:
        try:
            assert 0 <= r_index <= self.N
            assert 0 <= c_index <= self.N
            assert type(value) == float or type(value) == int
        except AssertionError:
            raise IndexError("Índice fora do intervalo, dotô")
        except TypeError:
            raise TypeError("Coloque somente números na matriz, dotô")
        
        self.data[r_index][c_index] = value


    def get_neighbours(self, index: int) -> list[float]:
        """
        Método para acessar a distância para as cidades a partir de uma origem, dada pelo índice
        """
        try:
            assert 0 <= index < self.N
        except AssertionError:
            raise IndexError("Índice fora do intervalo, dotô")
        
        return self.data[index]
    


