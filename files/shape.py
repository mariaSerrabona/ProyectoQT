from files.tetromione import Tetrominoe
# importación de las librerias
import random



#información de todas las posibles piezas del tetris
class Shape(object):
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, -1), (0, 0), (0, 1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, 1)),
        ((0, 0), (1, 0), (0, 1), (1, 1)),
        ((-1, -1), (0, -1), (0, 0), (0, 1)),
        ((1, -1), (0, -1), (0, 0), (0, 1))
    )

    #constructor
    def __init__(self):
        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)

    #getter de la figura
    def shape(self):
        return self.pieceShape
    #setter de la figura
    def setShape(self, shape):
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    #cada vez que se genera una figura, se elige de forma aleatoria
    def setRandomShape(self):
        self.setShape(random.randint(1, 7))
    #getter la coordenada x que ha ocupado la figura
    #se esta forma se puede saber si hay que eliminar la fila o si ya no caben mas figuras y el juego se ha terminado
    def x(self, index):
        return self.coords[index][0]

    #getter la coordenada y
    def y(self, index):
        return self.coords[index][1]

    #setter coordenada x
    def setX(self, index, x):
        self.coords[index][0] = x

    #setter de la coordenada y
    def setY(self, index, y):
        self.coords[index][1] = y


    #retorna el mínimo valor de x en el que la figura puede caer
    def minX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m
    #retorna el máximo valor de x en el que la figura puede caer
    def maxX(self):
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    #retorna el mínimo valor de y en el que la figura puede caer
    def minY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    #retorna el máximo valor de y en el que la figura puede caer
    def maxY(self):
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m


    #funciónes de rotación de la figura

    #se tiene que cambiar la disposición de la figura a la izquierda
    def rotateLeft(self):
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        #se invierten
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result


    #lo mismo pero hacia la derecha
    def rotateRight(self):
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result
