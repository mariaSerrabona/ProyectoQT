'''
en este ficheor se va a programar un juego de teris, empleando QT
'''

# importación de las librerias
import sys

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication

from files.board import Board
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
        self.setWindowTitle('Tetris de María')
        self.show()
    #función para que la ventana esté centrada en la pantalla
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2),
                    int((screen.height() - size.height()) / 2))



#función main que genera la aplicación QT
def main():

    app = QApplication([])
    tetris = Tetris()
    sys.exit(app.exec_())

#llamada del main
if __name__ == '__main__':
    main()

