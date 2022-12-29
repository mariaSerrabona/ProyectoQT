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

