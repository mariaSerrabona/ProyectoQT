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
    #funciín para que la ventana esté centrada en la pantalla
    def center(self):
        """centers the window on the screen"""

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                  int((screen.height() - size.height()) / 2))

