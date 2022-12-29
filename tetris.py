'''
en este ficheor se va a programar un juego de teris, empleando QT
'''

# importación de las librerias
import random
import sys

from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication


class Tetris(QMainWindow):

    #constructor de la clase
    def __init__(self):
        super().__init__()

        self.initUI()

    #función que inicia la aplicacion QT
    def initUI(self):
        # se establecen todos los witdgets de la ventana de inicio
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        #barra de estado para ver cuántas filas se han eliminado en la ejecución  del juego
        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.tboard.start()
        #dimensiones de la venatna de inicio y el nombre de la misma
        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()
    #función para que la ventana esté centrada en la pantalla
    def center(self):
        """centers the window on the screen"""

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                    int((screen.height() - size.height()) / 2))


#esta clase será la encargada de incicializar el juego
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


