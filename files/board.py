
# importación de las librerias

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QFrame
from files.tetromione import Tetrominoe
from files.shape import Shape


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    # se establecen parámetros básicos (ancho, alto y velocidad de figuras)
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    #función de inicio
    def initBoard(self):
        #se inicia el tiempo y va bajando la figura
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()


    #altura de la tabla
    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    #la froma de la tabla
    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    #ancho de la tabla
    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    #la altura de un cuadrado
    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    #se empieza el juego
    def start(self):
        #se para, se llama a la función de abajo
        if self.isPaused:
            return
        #se empieza si no está pausado
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.Speed, self)

    #acción de pausar el juego
    def pause(self):
        #Cuado se para, se puede inciar el juego de nuevo.
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()


    #IMPLEMENTACIÓN DE QT:

    # se emplea QPainter que es el responsable a un bajo nivel de dibujar en PyQt5.
    #se va a emplear para dibujar todas als posibles figuras del tetris
    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()


        # este proceso lo podemos dividir en dos acciones
        #primero se esbozarán los contornos de las figuras, en el caso de que no hayan sido ya definidas antes
        # en el caso de los cuadrados, las recordamos pero no las definimos porque ya lo hemos hecho antes
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    #ahora tenemmos que dibujar la pieza excta que va cayendo por el tablero
    def keyPressEvent(self, event):

        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        # en esta sección se definen las funciones que tienen cada tecla del teclado para poder jugar
        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        #a la derecha
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        #a la derecha
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        #a la izquierda
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        #con el espacio se va abajo directamente
        elif key == Qt.Key_Space:
            self.dropDown()

        #presionando la d, bajara la pieza un solo bloque (agiliza la caída de una forma no brusca)
        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)


    def timerEvent(self, event):
        """handles timer event"""

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()

        else:
            super(Board, self).timerEvent(event)

    def clearBoard(self):
        """clears shapes from the board"""

        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def dropDown(self):
        """drops down a shape"""

        newY = self.curY

        while newY > 0:

            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break

            newY -= 1

        self.pieceDropped()

    #con esta funció se genera una nueva pieza cuando la actual ya está abajo
    def oneLineDown(self):
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    #cada vez que una pieza cae, se comprueba si hay alguna linea completa para eliminarla
    def pieceDropped(self):
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())
        #si se puede, se elimina una linea completa
        self.removeFullLines()
        #si no, generamos una nueva pieza
        if not self.isWaitingAfterLine:
            self.newPiece()

    #función llamada en otras funciones para poder eliminar lineas completas
    def removeFullLines(self):
        numFullLines = 0
        rowsToRemove = []

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)
        #además, con cada línea completa eliminada es un punto más en nuestra partida
        if numFullLines > 0:
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()

    #función llamada en otras funciones para poder generar una nueva pieza aleatoria.
    def newPiece(self):
        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.curX = Board.BoardWidth // 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.timer.stop()
            self.isStarted = False
            #si ya no se pueden generar más piezas porque no caben, se acaba el juego
            self.msg2Statusbar.emit("Has perdido!")


    #se intentan mover las piezas, se retorna TRUE en el caso de que la pieza se pueda ubicar en el sitio seleccionado
    def tryMove(self, newPiece, newX, newY):
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    #función de estilos de las figuras
    def drawSquare(self, painter, x, y, shape):

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)
